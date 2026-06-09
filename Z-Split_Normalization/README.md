# Z-Split Normalization (Zero-Preserving Split Normalization)

**Author:** Abdulrhman Almoadi  
**Affiliation:** King Abdulaziz City for Science and Technology (KACST)  
**Version:** 1.0.0  
**License:** MIT

---

## Citation

If you use Z-Split, please cite:

> Almoadi, A.: Reducing False Alarms in Urban Flood Detection: An Enhanced NDWI (ENDWI) with Hybrid Max Fusion on Sentinel-2 Data, EGUsphere [preprint], https://doi.org/10.5194/egusphere-2026-672, 2026.

---

## The Problem

Bipolar spectral and spatial indices — such as NDWI, NDVI difference, and InSAR LOS displacement — share a critical property: **zero carries direct physical meaning** as the boundary between two classes (e.g., water vs. non-water, deformation vs. stability).

Standard normalization methods fail to preserve this boundary:

- **Min-Max** shifts zero by mapping the full range to [0, 1], destroying the class boundary and introducing artificial trends in multi-temporal analysis.
- **Z-Score** centers on the mean rather than zero, ignoring the physical significance of the zero boundary, and produces an unbounded output range unsuitable for Otsu thresholding.

When values are clustered in a narrow range near zero — as is common with NDWI in arid regions or InSAR LOS displacement over stable terrain — these distortions become critical: thresholding at zero becomes unreliable, and multi-temporal comparisons are corrupted by normalization artifacts rather than reflecting real change.

---

## The Solution — Z-Split

Z-Split normalizes each side of zero **independently**, stretching the full negative range to [−1, 0] and the full positive range to [0, 1], regardless of how narrow or skewed the original distribution is.

**This means:**
- Near-zero values are expanded into the full [−1, 1] range — not compressed to one end
- Zero is always exactly 0.000 — never shifted
- Otsu thresholding operates on a balanced, well-separated distribution
- Multi-temporal comparisons reflect real change, not normalization artifacts

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

## Validation

### 1. Optical Remote Sensing — Flood Detection

Tested on Sentinel-2 ENDWI flood data over Al-Laith Governorate, Saudi Arabia.

- Z-Split normalization reduced the False Alarm Rate (FAR) from **9.39% to 2.99%**
- Zero boundary fixed at 0.000 across all scenes
- Otsu threshold stability confirmed across multi-temporal acquisitions

### 2. InSAR LOS Displacement

Validated on InSAR Line-of-Sight displacement data where zero marks the boundary between surface uplift and subsidence.

- Stable pixel detection: **75.3%** (Z-Split) vs **26.6%** (Min-Max)
- Zero boundary preserved at 0.000 across all interferograms
- See `InSAR_Validation/` for full notebook and figures

### 3. Multi-Temporal Change Analysis — NDVI, Riyadh 2018–2024

Validated on four Sentinel-2 NDVI scenes (March–April, 2018–2020–2022–2024) over Riyadh, Saudi Arabia (scale: 10 m, 5603 × 5129 pixels per scene).

Three analyses were performed across 11,424 spatial patches and at pixel level:

#### A. Linear Trend (Slope per pixel, 2018–2024)

| Method | Mean Slope | Std | Correlation with Raw |
|--------|:----------:|:---:|:--------------------:|
| Raw (no normalization) | 0.000894 | 0.0165 | — |
| Min-Max | 0.027454 | 0.2170 | r = 0.511 |
| **Z-Split** | **−0.000120** | **0.0167** | **r = 0.995** |

Z-Split preserves the original temporal signal with **99.5% fidelity**, while Min-Max introduces artificial trends with a slope standard deviation **13× larger** than the raw data.

#### B. Anomaly Detection (2024 vs. multi-year mean)

Min-Max anomaly maps show spatially inverted patterns relative to raw data, indicating systematic distortion in year-to-year comparisons. Z-Split anomaly maps are visually and statistically consistent with raw anomaly patterns.

#### C. Coefficient of Variation (CV across 2018–2024)

| Method | Mean CV |
|--------|:-------:|
| Raw | 0.150 |
| **Z-Split** | **0.173** |
| Min-Max | 0.832 |

Min-Max inflates apparent temporal variability by **5.5×**, misclassifying stable pixels as highly variable. Z-Split maintains CV within 15% of the raw data baseline.

#### D. Threshold Stability (Otsu across 11,424 patches)

| Method | Threshold Std |
|--------|:-------------:|
| **Min-Max** | **0.0882** |
| Z-Split | 0.2220 |
| Z-Score | 1.2012 |

> **Note:** For NDVI over arid urban environments — where the distribution is strongly unipolar and bimodal — Min-Max threshold stability is comparable to Z-Split. Z-Split demonstrates its primary advantage in bipolar indices with narrow near-zero distributions (NDWI, InSAR LOS), consistent with its design objective.

---

## Application Scope

Z-Split is designed for **bipolar indices where zero carries physical meaning**. Its advantage is most pronounced when:

- Values are clustered in a narrow range near zero (e.g., NDWI in arid regions)
- Multi-temporal consistency is required (change detection, time series analysis)
- Otsu or zero-based thresholding is applied
- Cross-scene or cross-sensor comparisons are performed

For strongly unipolar indices (e.g., NDVI in vegetated regions), standard normalization methods may yield equivalent classification results, though Z-Split remains applicable without introducing distortion.

---

## Installation

```bash
pip install zsplit
```

## Code

```python
from zsplit import normalize

result = normalize(your_bipolar_index)
```

---

## Files

| File | Description |
|------|-------------|
| `zsplit_normalization.ipynb` | Jupyter Notebook with visual demonstration |
| `zsplit_arcpy.py` | ArcGIS Pro implementation |
| `InSAR_Validation/` | Validation on InSAR LOS displacement data |
| `Z-Split_Normalization/Validation/` | Multi-temporal NDVI change analysis |
| `Validation/01_Optical_ENDWI/` | Optical flood detection validation |

---

## Figures

**Figure 1:** Otsu threshold distribution across 11,424 spatial patches — Min-Max vs Z-Score vs Z-Split.

**Figure 2:** Multi-temporal NDVI change analysis (Linear Trend, Anomaly, CV) — Raw vs Min-Max vs Z-Split, Riyadh 2018–2024.

**Figure 3:** InSAR LOS displacement normalization comparison.
