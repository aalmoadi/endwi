# Z-Split Normalization (Zero-Preserving Split Normalization)

**Version:** 1.0.0  
**License:** MIT

---

## What is Z-Split?

Z-Split **preserves zero as a fixed physical boundary** while **expanding narrow distributions clustered around zero** into the full [−1, 1] range — normalizing and expanding in a single operation. This prevents the low-contrast output common with near-zero indices and creates a well-formed distribution suitable for Otsu thresholding and multi-temporal analysis.

---

## Core Idea and Motivation

Spectral indices and remote sensing operations often produce values clustered tightly around zero due to radiometric constraints, surface reflectance properties, or normalized difference formulations. Standard normalization compresses these values further, producing low-contrast images and unstable thresholds.

Z-Split expands each side of zero independently into [−1, 0] and [0, 1], simultaneously normalizing and stretching narrow distributions. This preserves distributional contrast for reliable thresholding, maintains the zero boundary across scenes for stable multi-temporal comparison, and broadens the practical utility of spectral indices in analytical workflows where near-zero clustering would otherwise limit accuracy.

---

## The Problem

Bipolar remote sensing indices share one property: **zero is a physical class boundary** (water/non-water, uplift/subsidence). Standard methods destroy it: Min-Max shifts zero into [0, 1]; Z-Score centers on the mean and produces an unbounded range. Both fail when values cluster near zero, making thresholding unreliable, multi-temporal comparisons artifact-driven, and in the worst case producing entirely empty, white, or black images due to values compressed around zero.

---

## The Solution — Z-Split

Z-Split normalizes each side of zero **independently**, stretching the full negative range to [−1, 0] and the full positive range to [0, 1].

### Formula

$$
Z\text{-}Split(x) =
\begin{cases}
x \;/\; \max(X^+) & \text{if } x > 0 \\
0 & \text{if } x = 0 \\
x \;/\; |\min(X^-)| & \text{if } x < 0
\end{cases}
$$

where $X^+$ is the set of positive values and $X^-$ is the set of negative values.  
**Output range:** [−1, 1] with zero strictly preserved.

---

## Why Z-Split?

| Property | Min-Max | Z-Score | Z-Split |
|----------|:-------:|:-------:|:-------:|
| Preserves zero as class boundary | ❌ | ❌ | ✅ |
| Expands narrow near-zero distributions | ❌ | ⚠️ | ✅ |
| Stable on skewed distributions | ❌ | ⚠️ | ✅ |
| Suitable for Otsu thresholding | ❌ | ⚠️ | ✅ |
| Multi-temporal direction preserved | ❌ | ❌ | ✅ |
| Output range | [0, 1] | Unbounded | [−1, 1] |

---

## Installation

```bash
pip install zsplit
```

## Quick Start

```python
from zsplit import normalize

result = normalize(your_bipolar_index)
```

---

## Validation

### 1. NDWI — Optical Remote Sensing

Tested on Sentinel-2 NDWI data. Z-Split successfully expanded near-zero clustered values while preserving the original image structure, producing contrast-enhanced output suitable for thresholding and multi-temporal comparison.

### 2. Multi-Temporal Change Analysis — NDVI, Riyadh 2018–2024

Validated on four Sentinel-2 NDVI scenes (March–April, 2018–2020–2022–2024) over Riyadh, Saudi Arabia (scale: 10 m, 5603 × 5129 pixels per scene) across 11,424 spatial patches.

#### A. Linear Trend (Slope per pixel, 2018–2024)

| Method | Mean Slope | Std | Correlation with Raw |
|--------|:----------:|:---:|:--------------------:|
| Raw (no normalization) | 0.000894 | 0.0165 | — |
| Min-Max | 0.027454 | 0.2170 | r = 0.511 |
| **Z-Split** | **−0.000120** | **0.0167** | **r = 0.995** |

Z-Split preserves the original temporal signal with **99.5% fidelity**. Min-Max introduces artificial trends with slope Std **13× larger** than raw data.

#### B. Anomaly Detection (2024 vs. multi-year mean)

Min-Max anomaly maps show spatially inverted patterns relative to raw data. Z-Split anomaly maps are visually and statistically consistent with raw data.

#### C. Coefficient of Variation (CV across 2018–2024)

| Method | Mean CV |
|--------|:-------:|
| Raw | 0.150 |
| **Z-Split** | **0.173** |
| Min-Max | 0.832 |

Min-Max inflates temporal variability by **5.5×**. Z-Split stays within 15% of the raw baseline.

#### D. Threshold Stability (Otsu across 11,424 patches)

| Method | Threshold Std |
|--------|:-------------:|
| Min-Max | 0.0882 |
| **Z-Split** | **0.2220** |
| Z-Score | 1.2012 |

> **Note:** For strongly unipolar NDVI in arid urban areas, Min-Max threshold stability is comparable to Z-Split. Z-Split's primary advantage is in bipolar indices with narrow near-zero distributions (NDWI, InSAR LOS), consistent with its design objective.

---

## Application Scope

Most effective when:
- Values cluster near zero (NDWI in arid regions, InSAR LOS over stable terrain)
- Multi-temporal consistency is required
- Otsu or zero-based thresholding is applied
- Cross-scene or cross-sensor comparisons are performed

---

## Files

| File | Description |
|------|-------------|
| `zsplit_normalization.ipynb` | Jupyter Notebook with visual demonstration |
| `zsplit_arcpy.py` | ArcGIS Pro implementation |
| `Z-Split_Normalization/Validation/` | Multi-temporal NDVI change analysis |
| `Validation/01_Optical_ENDWI/` | Optical NDWI validation |

---

## Figures

**Figure 1:** Otsu threshold distribution across 11,424 spatial patches — Min-Max vs Z-Score vs Z-Split.

**Figure 2:** Multi-temporal NDVI change analysis (Linear Trend, Anomaly, CV) — Raw vs Min-Max vs Z-Split, Riyadh 2018–2024.

---

## Author

**Abdulrhman Almoadi**  
King Abdulaziz City for Science and Technology (KACST)

---

## Citation

If you use Z-Split, please cite:

> Almoadi, A.: Reducing False Alarms in Urban Flood Detection: An Enhanced NDWI (ENDWI) with Hybrid Max Fusion on Sentinel-2 Data, EGUsphere [preprint], https://doi.org/10.5194/egusphere-2026-672, 2026.
