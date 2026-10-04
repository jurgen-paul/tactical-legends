#!/usr/bin/env python3
"""
CSS for Supporter Tiers - Stylesheet and Generator
"""

CSS_CONTENT = """
.supporters {
  margin: 80px 0;
  text-align: center;
  color: #00ff88;
}

.supporters h2 {
  font-size: 2.5rem;
  font-family: 'Orbitron', monospace;
  margin-bottom: 30px;
  text-shadow: 0 0 10px rgba(0, 255, 136, 0.6);
}

.tiers {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  gap: 30px;
}

.tier {
  background: rgba(10, 10, 10, 0.8);
  border: 2px solid #00ff88;
  border-radius: 12px;
  padding: 30px;
  width: 280px;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
  box-shadow: 0 0 20px rgba(0, 255, 136, 0.2);
}

.tier:hover {
  transform: translateY(-8px);
  box-shadow: 0 0 30px rgba(0, 255, 136, 0.4);
}

.tier h3 {
  font-size: 1.8rem;
  font-family: 'Orbitron', monospace;
  margin-bottom: 15px;
}

.tier .price {
  font-size: 1.5rem;
  color: #38bdf8;
  margin-bottom: 20px;
  font-weight: 700;
}

.tier ul {
  list-style: none;
  padding: 0;
  margin-bottom: 25px;
}

.tier li {
  margin: 10px 0;
  color: #94a3b8;
}
"""


def get_css() -> str:
    """Returns the CSS styling string for supporter tiers."""
    return CSS_CONTENT.strip()


if __name__ == "__main__":
    print(get_css())
