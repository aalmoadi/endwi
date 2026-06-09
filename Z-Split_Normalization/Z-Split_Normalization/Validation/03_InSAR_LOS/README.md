# Z-Split Validation — InSAR LOS Displacement

## Dataset
- Simulated LOS Displacement Time Series
- 10 scenes — 100x100 pixels
- Range: -41.70 to +28.70 mm

## Results

| Method | Stable Detection% | Zero Boundary |
|---|---|---|
| Min-Max | 26.6% | 0.592–0.652 (varies) |
| **Z-Split** | **75.3%** | **0.000 (fixed)** |
| True Stable | 80.9% | — |

## Key Finding
Min-Max zero boundary varied between 0.592 and 0.652 across scenes —
making temporal comparisons unreliable.
Z-Split maintained a fixed zero boundary across all 10 scenes,
correctly identifying 75.3% of stable pixels vs 26.6% for Min-Max.

## Files
- zsplit_insar_los_validation.ipynb — Full analysis notebook
- los_zsplit_comparison.png — Visual comparison
