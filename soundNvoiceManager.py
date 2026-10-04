#!/usr/bin/env python3
"""
Tactical Legends - Voice & Sound Engine
Manages cinematic trailer audio scripts, ElevenLabs/Play.ht generation manifests,
and synthesized WAV sound generation using standard Python library.
"""

import json
import math
import struct
import wave
from dataclasses import dataclass, field
from pathlib import Path
from typing import List, Dict, Any, Optional


@dataclass
class VoiceLine:
    scene: int
    filename: str
    text: str
    character: str = "Narrator"
    tone: str = "Cinematic"


class SoundNVoiceManager:
    def __init__(self, voice_id: str = "Antoni", model_id: str = "eleven_multilingual_v2"):
        self.voice_id = voice_id
        self.model_id = model_id
        self.items: List[VoiceLine] = [
            VoiceLine(1, "scene01_0000-0005.mp3", "In the cratered hush after the orbital dawn… a shadow walks.", "Narrator", "Low, gravelly"),
            VoiceLine(2, "scene02_0006-0015.mp3", "Born in the wreckage of the Orbital Institute of Strategic Tactics… they call her… the Echo of Forgotten Wars.", "Narrator", "Solemn"),
            VoiceLine(3, "scene03_0016-0025.mp3", "A mind that reads a battlefield like a weather report… and a heart bound by an oath only trust can unlock.", "Narrator", "Focused"),
            VoiceLine(4, "scene04_0026-0036.mp3", "Something in memory logs is trying to surface.", "Zoe", "Digital glitch, soft"),
            VoiceLine(5, "scene05_0037-0050.mp3", "Will you follow the voice… and earn their trust? Or silence it… and embrace the ruthless path?", "Narrator", "Tense, building"),
            VoiceLine(6, "scene06_0051-0105.mp3", "Memories are keys. Each one opens a door… or seals it forever.", "OISTARIAN", "Whispered, resolute"),
            VoiceLine(7, "scene07_0106-0120.mp3", "In the cathedral of data, the past will speak… and the future will answer.", "Narrator", "Dramatic climax"),
            VoiceLine(8, "scene08_0121-0130.mp3", "ECHOES OF OISTARIAN. Every choice leaves… an echo.", "Narrator", "Final beat")
        ]

    def to_manifest(self) -> Dict[str, Any]:
        return {
            "voice_id": self.voice_id,
            "model_id": self.model_id,
            "items": [
                {
                    "scene": item.scene,
                    "filename": item.filename,
                    "text": item.text,
                    "character": item.character,
                    "tone": item.tone
                }
                for item in self.items
            ]
        }

    def generate_synth_wav(self, output_path: str, frequency: float = 220.0, duration: float = 1.0, sample_rate: int = 44100):
        """Generates a pure sine/harmonic waveform WAV file using Python's standard wave library."""
        num_samples = int(duration * sample_rate)
        wav_file = wave.open(output_path, "w")
        wav_file.setparams((1, 2, sample_rate, num_samples, "NONE", "not compressed"))

        values = []
        for i in range(num_samples):
            t = float(i) / sample_rate
            # Dual sine overtone for sci-fi pulse sound
            sample = math.sin(2.0 * math.pi * frequency * t) * 0.7 + math.sin(2.0 * math.pi * frequency * 2 * t) * 0.3
            # Exponential decay envelope
            envelope = math.exp(-3.0 * t / duration)
            sample_val = int(sample * envelope * 32767.0 * 0.5)
            packed_val = struct.pack("h", max(-32768, min(32767, sample_val)))
            values.append(packed_val)

        wav_file.writeframes(b"".join(values))
        wav_file.close()

    def print_script(self):
        print(f"=== TACTICAL LEGENDS VOICE MANIFEST [{self.voice_id}] ===")
        for item in self.items:
            print(f"[{item.scene:02d}] {item.character.upper()}: \"{item.text}\" ({item.tone})")


if __name__ == "__main__":
    manager = SoundNVoiceManager()
    manager.print_script()
    print("\nManifest JSON:")
    print(json.dumps(manager.to_manifest(), indent=2))
