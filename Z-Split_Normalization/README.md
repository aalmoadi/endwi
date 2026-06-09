# Z-Split Normalization (Zero-Preserving Split Normalization)

**Author:** Abdulrhman Almoadi  
**Affiliation:** King Abdulaziz City for Science and Technology (KACST)

## Citation
If you use Z-Split, please cite:
> Almoadi, A.: Reducing False Alarms in Urban Flood Detection: An Enhanced NDWI (ENDWI) with Hybrid Max Fusion on Sentinel-2 Data, EGUsphere [preprint], https://doi.org/10.5194/egusphere-2026-672, 2026.

---

## What is Z-Split?

Z-Split is a normalization technique for bipolar spectral indices where zero carries physical meaning as a class boundary.

**Formula:**
- Positive values → [0, 1]
- Negative values → [-1, 0]  
- Zero → strictly preserved as 0

---

## Why Z-Split?

| Method | Mean Error% | Zero Preserved |
|---|---|---|
| Min-Max | 3.00% | ❌ |
| Z-Score | 2.10% | ❌ |
| **Z-Split** | **0.10%** | **✅** |

---

## Validation

### Optical Remote Sensing
- Tested on Sentinel-2 ENDWI flood data
- FAR reduced from 9.39% to 2.99%

### InSAR LOS Displacement
- Stable pixel detection: 75.3% vs 26.6% for Min-Max
- Zero boundary fixed at 0.000 across all scenes

---

## Files

- **zsplit_normalization.ipynb** — Jupyter Notebook with visual demonstration
- **zsplit_arcpy.py** — ArcGIS Pro implementation
- **InSAR_Validation/** — Validation on InSAR LOS data
- **Optical_Validation/** — Five systematic tests on optical data

---

## Code

```python
from zsplit import normalize
result = normalize(your_bipolar_index)
```
