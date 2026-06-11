# synthetic_eeg_cases_24/syntheticeeg_cases_24.py

import numpy as np
from pathlib import Path

OUTPUT_DIR = Path("synthetic_eeg_cases_24/generated_cases")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

def generate_eye_blink(fs=256, duration=2.0):
    t = np.linspace(0, duration, int(fs * duration), endpoint=False)
    signal = np.exp(-((t - duration / 2) ** 2) / 0.01)  # sharp central pulse
    return signal

def generate_line_noise(fs=256, duration=2.0, freq=60):
    t = np.linspace(0, duration, int(fs * duration), endpoint=False)
    return 0.2 * np.sin(2 * np.pi * freq * t)

def generate_electrode_drop(fs=256, duration=2.0):
    signal = np.ones(int(fs * duration))
    signal[int(len(signal)/2):] = 0
    return signal

def save_signal(signal, name):
    path = OUTPUT_DIR / f"{name}.npy"
    np.save(path, signal)
    print(f"✅ Saved: {path.resolve()}")

def main():
    save_signal(generate_eye_blink(), "eye_blink")
    save_signal(generate_line_noise(), "line_noise")
    save_signal(generate_electrode_drop(), "electrode_drop")

if __name__ == "__main__":
    main()
