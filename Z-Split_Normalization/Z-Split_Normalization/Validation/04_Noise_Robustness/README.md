# Z-Split Validation — Noise Robustness

## Dataset
- Simulated bipolar index data
- Near-zero clustering (ENDWI-like)
- Noise levels: 0.000 to 0.050

## Results

| Noise Level | Min-Max Error% | Z-Split Error% |
|---|---|---|
| 0.000 (clean) | 14.00% | **0.10%** |
| 0.001 | 12.60% | **0.10%** |
| 0.005 | **16.50%** | **0.10%** |
| 0.010 | 12.70% | **0.10%** |
| 0.020 | 4.30% | **0.10%** |
| 0.050 | 6.30% | **0.10%** |

## Key Finding
Z-Split maintained a consistent error of 0.10% across all noise levels.
Min-Max error peaked at 16.50% at moderate noise — non-monotonic and
unpredictable behavior that makes it unreliable for real-world data.

## Critical Observation
Min-Max error was highest at moderate noise (0.005) — not at maximum noise.
This unpredictable behavior is fundamentally unsuitable for automated
classification pipelines.
