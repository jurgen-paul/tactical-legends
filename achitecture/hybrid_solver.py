import os
import logging
import math
import kaggle_evaluation.aimo_3_inference_server
import pandas as pd
import polars as pl

# Optional dependencies used by the hybrid solver
import sympy as sp
import torch
import torch.nn as nn
from transformers import AutoTokenizer, AutoModel


# ============================================================
# Logging setup
# ============================================================
def setup_logging(level: int = logging.INFO):
    logging.basicConfig(
        level=level,
        format="%(asctime)s [%(levelname)s] %(message)s",
        handlers=[logging.StreamHandler()]
    )


setup_logging()


# ============================================================
# Utility functions
# ============================================================
def clamp_int(value: int, low: int = 0, high: int = 99999) -> int:
    """ Clamp integer to competition bounds."""
    return max(low, min(high, int(value)))


def is_numeric_string(s: str) -> bool:
    """Check if string looks like a numeric literal."""
    try:
        float(str(s).strip())
        return True
    except Exception:
        return False


def sanitize_sympy_result(res) -> int | None:
    """
    Convert SymPy result to an int if sensible.
    Returns None if not a finite numeric value.
    """
    try:
        # Evaluate numeric
        val = float(sp.N(res))
        if math.isfinite(val):
            # Round to nearest integer for competition
            return int(round(val))
        return None
    except Exception:
        return None


def score_sympy_confidence(question: str, parse_success: bool, result: int | None) -> float:
    """
    Heuristic confidence for SymPy:
    - Start from 0.5 for parse success, 0.1 for parse failure
    - Boost if the question looks symbolic (digits, operators)
    - Increase if the result is within bounds
    """
    base = 0.5 if parse_success else 0.1
    symbolic_hint = 0.2 if any(ch in question for ch in "+-*/^=()[]") or any(c.isdigit() for c in question) else 0.0
    bounds_bonus = 0.2 if (result is not None and 0 <= result <= 99999) else 0.0
    return max(0.0, min(1.0, base + symbolic_hint + bounds_bonus))


def score_torch_confidence(raw_output: float) -> float:
    """
    Heuristic confidence for Torch regression:
    - Penalise extremes or NaNs
    - Higher confidence near integer-like values
    """
    if raw_output is None or not math.isfinite(raw_output):
        return 0.0
    # Distance to nearest integer
    frac_dist = abs(raw_output - round(raw_output))
    proximity = max(0.0, 1.0 - min(1.0, frac_dist))  # 1 if near integer, down to 0
    # Penalise outside bounds
    if raw_output < -1000 or raw_output > 110000:
        penalty = 0.5
    else:
        penalty = 0.0
    return max(0.0, min(1.0, proximity - penalty + 0.3))  # add base 0.3


def choose_with_confidence(sympy_result: int | None, sympy_conf: float,
                           torch_result: int, torch_conf: float) -> int:
    """
    The final answer uses confidence and sanity checks.
    - Prefer SymPy if confidence is significantly higher and the result is sane.
    - Otherwise, pick Torch.
    """
    logging.info(f"Decision: SymPy(res={sympy_result}, conf={sympy_conf:.2f}) "
                 f"vs Torch(res={torch_result}, conf={torch_conf:.2f})")

    sympy_sane = sympy_result is not None and 0 <= sympy_result <= 99999
    torch_sane = 0 <= torch_result <= 99999

    if sympy_sane and (sympy_conf >= torch_conf + 0.15):
        return sympy_result
    if not torch_sane and sympy_sane:
        return sympy_result
    if not sympy_sane and torch_sane:
        return torch_result

    # Both sane or both questionable: prefer higher confidence
    if sympy_conf > torch_conf:
        return sympy_result if sympy_sane else clamp_int(sympy_result or 0)
    else:
        return torch_result if torch_sane else clamp_int(torch_result)


# ============================================================
# Torch head definition
# ============================================================
class RegressionHead(nn.Module):
    """
    Simple regression head mapping transformer hidden size to a single scalar.
    Replace or extend as needed.
    """
    def __init__(self, hidden_size: int):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(hidden_size, 512),
            nn.ReLU(),
            nn.Linear(512, 128),
            nn.ReLU(),
            nn.Linear(128, 1)
        )

    def forward(self, x):
        return self.net(x)


# ============================================================
# Hybrid solver
# ============================================================
class HybridSolver:
    """
    SymPy-first solver with fallback to transformer embeddings + PyTorch regression.
    Includes logging, confidence scoring, and bounds enforcement.
    """
    def __init__(self,
                 model_path: str | None = None,
                 transformer_name: str = "bert-base-uncased",
                 device: str = "cpu",
                 max_length: int = 512):
        self.device = torch.device(device)
        logging.info("Initializing transformer components...")
        self.tokenizer = AutoTokenizer.from_pretrained(transformer_name)
        self.encoder = AutoModel.from_pretrained(transformer_name).to(self.device)
        hidden_size = self.encoder.config.hidden_size

        logging.info("Initializing PyTorch regression head...")
        self.regression = RegressionHead(hidden_size).to(self.device)

        if model_path and os.path.exists(model_path):
            logging.info(f"Loading regression weights from {model_path}")
            state = torch.load(model_path, map_location=self.device)
            self-regression.load_state_dict(state)
        else:
            logging.warning("No regression weights found; using randomly initialized head.")

        self-regression.eval()
        self.max_length = max_length

    # ---------------------------
    # SymPy path
    # ---------------------------
    def try_sympy(self, question: str) -> tuple[int | None, float]:
        """
        Attempt to parse and evaluate with SymPy, return (result, confidence).
        """
        logging.info("Trying SymPy...")
        parse_success = False
        result_int = None

        try:
            # Fast pass: if the question is a plain numeric string
            if is_numeric_string(question):
                result_int = int(round(float(question.strip())))
                parse_success = True
            else:
                # Attempt symbolic parsing
                expr = sp.sympify(question)
                parse_success = True
                result_int = sanitize_sympy_result(expr.evalf())
        except Exception as e:
            logging.debug(f"SymPy parsing/evaluation failed: {e}")

        conf = score_sympy_confidence(question, parse_success, result_int)
        logging.info(f"SymPy result={result_int}, confidence={conf:.2f}")
        return result_int, conf

    # ---------------------------
    # Transformer + Torch path
    # ---------------------------
    def torch_infer(self, question: str) -> tuple[int, float]:
        """
        Encode with a transformer and predict with a regression head.
        Returns (clamped_int_result, confidence).
        """
        logging.info("Falling back to transformer + PyTorch...")
        inputs = self.tokenizer(
            question,
            return_tensors="pt",
            truncation=True,
            padding=True,
            max_length=self.max_length
        ).to(self.device)

        with a torch.no_grad():
            enc_out = self.encoder(**inputs)
            # Use CLS token embedding for pooled representation
            clsemb = enc_out.last_hidden_state[:, 0, :]  # [batch, hidden]
            raw = self.regression(cls_emb).squeeze(-1)    # [batch]
            raw_val = float(raw.item())

        conf = score_torch_confidence(raw_val)
        result = clamp_int(round(raw_val))
        logging.info(f"Torch raw={raw_val:.4f}, clamped={result}, confidence={conf:.2f}")
        return result, conf

    # ---------------------------
    # Unified predict
    # ---------------------------
    def predict(self, question: str) -> int:
        """
        Hybrid decision:
        1) Try SymPy; if confident and sane, return.
        2) Otherwise, get Torch result.
        3) Choose between both using confidence and sanity checks.
        """
        # Guardrails on input
        if not isinstance(question, str) or not question.strip():
            logging.warning("Empty or invalid question string; returning 0.")
            return 0

        sympy_result, sympy_conf = self.try_sympy(question)
        torch_result, torch_conf = self.torch_infer(question)

        final = choose_with_confidence(sympy_result, sympy_conf, torch_result, torch_conf)
        final = clamp_int(final)
        logging.info(f"Final decision: {final}")
        return final


# ============================================================
# Kaggle integration
# ============================================================
# Choose your solver:
# - Provide your trained regression head weights via model_path if available.
model = HybridSolver(
    model_path="/kaggle/input/my-trained-model/model.pt",  # adjust or set to None
    transformer_name="bert-base-uncased",
    device="cpu",
    max_length=512
)


def predict(id_: pl.Series, problem: pl.Series) -> pl.DataFrame | pd.DataFrame:
    """Competition-required predict() signature."""
    # Unpack single row inputs
    id_val = id_.item(0)
    problem_text: str = problem.item(0)

    # Run hybrid model
    prediction = model.predict(problem_text)

    # Return schema-compliant result
    return pl.DataFrame({"id": id_val, "answer": prediction})


# ============================================================
# Inference server
# ============================================================
inference_server = kaggle_evaluation.aimo_3_inference_server.AIMO3InferenceServer(predict)

if os.getenv("KAGGLE_IS_COMPETITION_RERUN"):
    inference_server.serve()
else:
    inference_server.run_local_gateway((
        "/kaggle/input/ai-mathematical-olympiad-progress-prize-3/test.csv",
    ))
