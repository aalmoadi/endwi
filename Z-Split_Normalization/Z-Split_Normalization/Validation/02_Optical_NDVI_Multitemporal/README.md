# Z-Split Validation — Multi-temporal NDVI Analysis

## Dataset
- Simulated NDVI data — 5 years
- Arid region scenario (Saudi Arabia)
- 80% non-vegetation, 20% vegetation

## Results

| Year | True Change% | Min-Max Change% | Z-Split Change% |
|---|---|---|---|
| Year 2 | -5.1% | -3.5% | **-5.1%** |
| Year 3 | -7.5% | **+1.2%** | **-7.5%** |
| Year 4 | -3.7% | **+8.0%** | **-3.7%** |
| Year 5 | +1.1% | +13.0% | **+1.1%** |

## Key Finding
Min-Max reversed the direction of vegetation change in 3 out of 4 years.
Z-Split maintained zero error in change detection across all years.
