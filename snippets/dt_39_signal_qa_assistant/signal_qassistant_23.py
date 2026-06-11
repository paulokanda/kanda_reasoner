import numpy as np

def score_viewability(signal: np.ndarray, fs: float = 256.0) -> dict:
    """
    Scores EEG signal segment for viewability. Returns a dict with heuristic quality metrics.

    Parameters:
    - signal: 1D NumPy array of EEG values
    - fs: sampling frequency

    Returns:
    - Dict with score between 0-1, suggested adjustments
    """
    if signal.ndim != 1:
        raise ValueError("Signal must be a 1D array")

    snr = np.mean(signal) / (np.std(signal) + 1e-6)
    power = np.mean(signal ** 2)
    zero_crossings = np.count_nonzero(np.diff(np.sign(signal)))
    complexity = zero_crossings / len(signal)

    score = min(1.0, snr / 2 + complexity + power / 5000)

    advice = []
    if snr < 0.5:
        advice.append("Try bandpass filtering (e.g., 1–40 Hz).")
    if complexity < 0.01:
        advice.append("Signal may be flat — check electrodes or gain.")
    if power > 1e5:
        advice.append("High power — apply notch filter or rescale.")

    return {
        "score": round(score, 2),
        "snr": round(snr, 2),
        "complexity": round(complexity, 4),
        "power": round(power, 2),
        "advice": advice
    }

# Example test
if __name__ == "__main__":
    fake = np.sin(np.linspace(0, 20*np.pi, 1024)) + 0.1*np.random.randn(1024)
    result = score_viewability(fake)
    for k, v in result.items():
        print(f"{k}: {v}")
