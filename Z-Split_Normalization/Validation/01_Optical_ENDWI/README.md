
# Z-Split Validation — Optical ENDWI (Sentinel-2)

## Dataset
- Sentinel-2 Level-2A
- Al-Lith Governorate, Saudi Arabia
- Flash flood event: November 2018
- Validation points: 1,262 (559 flooded, 703 non-flooded)

## Results

| Method | FAR% | Precision% | OA% |
|---|---|---|---|
| Raw ENDWI | 9.39% | 89.44% | 94.77% |
| **Z-Split** | **2.99%** | **96.37%** | **98.26%** |

## Key Finding
Z-Split reduced FAR by 68% on real Sentinel-2 flood data.
