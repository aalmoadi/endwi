# Z-Split Normalization (Zero-Preserving Split Normalization)

**Version:** 1.0.1  
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

## Practical Applications in Remote Sensing

Z-Split addresses a critical problem in any workflow involving bipolar indices across time or sensors:

**1. Change Detection**  
Applying Min-Max before change detection introduces artificial trends that appear as land cover change but reflect only normalization artifacts. A report showing "15% vegetation decline" may be entirely attributable to normalization, not reality.

**2. Time Series Analysis**  
Studies tracking floods, drought, or urban expansion over time require a clean temporal signal. Min-Max corrupts this signal by rescaling each scene independently to [0, 1], making year-to-year comparisons unreliable.

**3. Multi-temporal Machine Learning**  
Models trained on Min-Max normalized multi-year data learn spurious patterns introduced by normalization rather than real spectral change. Z-Split ensures the training signal reflects actual surface conditions.

**4. InSAR and Displacement Monitoring**  
In LOS displacement data, zero means no movement. Shifting zero through Min-Max misclassifies stable pixels as deforming, directly corrupting subsidence or uplift maps.

---

## Validation

### 1. NDWI — Optical Remote Sensing

Tested on Sentinel-2 NDWI data. Z-Split successfully expanded near-zero clustered values while preserving the original image structure, producing contrast-enhanced output suitable for thresholding and multi-temporal comparison.

### 2. Multi-Temporal Change Analysis — NDVI, Riyadh 2018–2024

Validated on four Sentinel-2 NDVI scenes (March–April, 2018–2020–2022–2024) over Riyadh, Saudi Arabia (scale: 10 m, 5603 × 5129 pixels per scene) across 11,424 spatial patches.

#### A. Normalization Artifact Analysis

The figure below shows the deviation of each normalization method from the raw temporal signal. Min-Max introduces large artificial trends across the entire scene (colored map). Z-Split introduces virtually no deviation (near-white map).

![Deviation Analysis](https://raw.githubusercontent.com/aalmoadi/endwi/main/Figures/deviation_analysis.png)

| Method | Mean Absolute Deviation | Std |
|--------|:-----------------------:|:---:|
| Min-Max | 0.1858 | 0.2091 |
| **Z-Split** | **0.0013** | **0.0017** |

Z-Split preserves the temporal signal with **143× greater fidelity** than Min-Max.

#### B. Linear Trend (Slope per pixel, 2018–2024)

| Method | Mean Slope | Std | Correlation with Raw |
|--------|:----------:|:---:|:--------------------:|
| Raw (no normalization) | 0.000894 | 0.0165 | — |
| Min-Max | 0.027454 | 0.2170 | r = 0.511 |
| **Z-Split** | **−0.000120** | **0.0167** | **r = 0.995** |

#### C. Multi-Temporal Change Maps

The figure below compares Linear Trend, Anomaly, and Coefficient of Variation maps across all three methods. Z-Split maps are visually and statistically consistent with raw data; Min-Max maps show spatially inverted anomaly patterns and 5.5× inflated variability.

![Change Analysis](https://raw.githubusercontent.com/aalmoadi/endwi/main/Figures/change_analysis.png)

| Method | Mean CV |
|--------|:-------:|
| Raw | 0.150 |
| **Z-Split** | **0.173** |
| Min-Max | 0.832 |

#### D. Threshold Stability (Otsu across 11,424 patches)

| Method | Threshold Std |
|--------|:-------------:|
| Min-Max | 0.0882 |
| Z-Split | 0.2220 |
| Z-Score | 1.2012 |

> **Note:** For strongly unipolar NDVI in arid urban areas, Min-Max threshold stability is comparable to Z-Split. Z-Split's primary advantage is in bipolar indices with narrow near-zero distributions (NDWI, InSAR LOS), consistent with its design objective.

---

## Application Scope

Most effective when:
- Values cluster near zero (NDWI in arid regions, InSAR LOS over stable terrain)
- Multi-temporal consistency is required (change detection, time series analysis)
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

## Author

**Abdulrhman Almoadi**  
King Abdulaziz City for Science and Technology (KACST)

---

## Citation

If you use Z-Split, please cite:

> Almoadi, A.: Reducing False Alarms in Urban Flood Detection: An Enhanced NDWI (ENDWI) with Hybrid Max Fusion on Sentinel-2 Data, EGUsphere [preprint], https://doi.org/10.5194/egusphere-2026-672, 2026.
