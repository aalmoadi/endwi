# ENDWI — Enhanced Normalized Difference Water Index

[![DOI](https://zenodo.org/badge/1037018439.svg)](https://doi.org/10.5281/zenodo.20602709)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**Author:** Abdulrhman Almoadi  
**Affiliation:** King Abdulaziz City for Science and Technology (KACST), Riyadh, Saudi Arabia

---

## Overview

This repository contains the code and data supporting the manuscript:

> Almoadi, A.: Reducing False Alarms in Urban Flood Detection: An Enhanced NDWI (ENDWI) with Hybrid Max Fusion on Sentinel-2 Data, EGUsphere [preprint], https://doi.org/10.5194/egusphere-2026-672, 2026.

The study proposes two original contributions:

1. **ENDWI** (Enhanced Normalized Difference Water Index) — a novel spectral water index formulated as NDWI divided by the Green band, designed to suppress urban false alarms in flood detection.
2. **Z-Split** (Zero-Preserving Split Normalization) — a normalization technique that expands the narrow dynamic range of ENDWI while strictly preserving zero as the natural water/non-water class boundary.

---

## ENDWI Formula

```
ENDWI = NDWI / Green = [(Green − NIR) / (Green + NIR)] / Green
```

Applied to Sentinel-2 imagery (Bands: B03, B08).

---

## Z-Split Formula

$$
Z_{\text{split}}(x) =
\begin{cases}
x \;/\; \max(X^+) & \text{if } x > 0 \\
0 & \text{if } x = 0 \\
x \;/\; |\min(X^-)| & \text{if } x < 0
\end{cases}
$$

Output range: **[−1, 1]** with zero strictly preserved.

---

## Key Results

| Method | Overall Accuracy | Precision | FAR |
|---|---|---|---|
| Hybrid Max (ENDWI + AWEIsh) | 82.65% | **94.50%** | **2.99%** |
| ENDWI_otsu | 73.14% | 79.41% | 10.95% |
| AWEIsh_otsu | 81.14% | 76.10% | 20.91% |
| NDWI_otsu | 61.09% | 55.67% | 37.84% |

FAR = FP / (FP + TN) — validated against 1,262 ground-truth points (559 flooded + 703 non-flooded) from WorldView-4 imagery, Al-Lith Governorate, Saudi Arabia.

---

## Repository Structure

```
endwi/
├── Data/                        # Sample input data
├── Figures/                     # Manuscript figures
├── Ground Truth Points/         # Validation points
├── Independent_Validation/      # Independent flood event validation
├── InSAR_Validation/            # Z-Split applied to InSAR data
├── Z-Split_Normalization/       # Z-Split code and validation
│   ├── zsplit_normalization.ipynb   # Jupyter notebook (main demo)
│   ├── zsplit_arcpy.py              # ArcGIS Pro script
│   ├── los_zsplit_comparison.png    # Histogram comparison figure
│   └── Validation/              # Validation experiments
│       ├── 02_Optical_NDVI_Multitemporal/
│       ├── 03_InSAR_LOS/
│       └── 04_Noise_Robustness/
├── Z-Split Normalization.ipynb  # Top-level notebook
├── LICENSE
└── README.md
```

---

## Requirements

```
Python >= 3.8
numpy
rasterio
matplotlib
```

Install dependencies:

```bash
pip install numpy rasterio matplotlib
```

For the ArcGIS Pro script (`zsplit_arcpy.py`), ArcGIS Pro with the Spatial Analyst extension is required.

---

## Usage

### Python (Jupyter Notebook)

Open `Z-Split_Normalization/zsplit_normalization.ipynb` and follow the cells. A synthetic data demo is included in Section 6 — no raster files needed.

### ArcGIS Pro

1. Open `Z-Split_Normalization/zsplit_arcpy.py`
2. Update `INPUT_RASTER` and `OUTPUT_RASTER` paths
3. Run from the ArcGIS Pro Python window

---

## Citation

If you use ENDWI or Z-Split in your research, please cite:

```
Almoadi, A.: Reducing False Alarms in Urban Flood Detection: An Enhanced NDWI (ENDWI)
with Hybrid Max Fusion on Sentinel-2 Data, EGUsphere [preprint],
https://doi.org/10.5194/egusphere-2026-672, 2026.
```

---

## License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.
