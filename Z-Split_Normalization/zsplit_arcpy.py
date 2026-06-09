# =============================================================================
# zsplit_arcpy.py
# Z-Split Normalization (Zero-Preserving Split Normalization) for ArcGIS Pro
#
# Author : Abdulrhman Almoadi
# Affil. : King Abdulaziz City for Science and Technology (KACST)
# Repo   : https://github.com/aalmoadi/endwi
#
# Citation
# --------
# Almoadi, A.: Reducing False Alarms in Urban Flood Detection: An Enhanced
# NDWI (ENDWI) with Hybrid Max Fusion on Sentinel-2 Data, EGUsphere [preprint],
# https://doi.org/10.5194/egusphere-2026-672, 2026.
#
# Description
# -----------
# Applies Z-Split normalization to a raster in ArcGIS Pro using arcpy and
# the Spatial Analyst Raster Calculator. Zero is strictly preserved as the
# natural class boundary (water / non-water).
#
# Formula
# -------
#   if x > 0 : x / max(positive values)   → [0,  1]
#   if x = 0 : 0                           → 0
#   if x < 0 : x / |min(negative values)| → [-1, 0]
#
# Requirements
# ------------
#   - ArcGIS Pro with Spatial Analyst extension
#   - arcpy (available inside ArcGIS Pro Python environment)
#
# Usage
# -----
#   Run directly in ArcGIS Pro Python window, or as a standalone script
#   from the ArcGIS Pro conda environment.
# =============================================================================

import arcpy
from arcpy.sa import Raster, Con, IsNull
import numpy as np
import os

arcpy.CheckOutExtension("Spatial")
arcpy.env.overwriteOutput = True


# =============================================================================
# USER INPUTS — update these paths before running
# =============================================================================

INPUT_RASTER  = r"/path/to/your/ENDWI_raw.tif"
OUTPUT_RASTER = r"/path/to/your/ENDWI_zsplit.tif"

# Snap raster / environment (optional — set to INPUT_RASTER if unsure)
SNAP_RASTER   = INPUT_RASTER


# =============================================================================
# ENVIRONMENT SETTINGS
# =============================================================================

arcpy.env.snapRaster = SNAP_RASTER
arcpy.env.extent     = SNAP_RASTER
arcpy.env.cellSize   = SNAP_RASTER


# =============================================================================
# CORE FUNCTION
# =============================================================================

def zsplit_normalize_arcpy(input_raster_path, output_raster_path):
    """
    Apply Z-Split normalization to a raster using arcpy + NumPy.

    Parameters
    ----------
    input_raster_path  : str — path to input raster (e.g., raw ENDWI .tif)
    output_raster_path : str — path where normalized raster will be saved

    Returns
    -------
    output_raster_path : str — path to saved output raster
    """

    print(f"Loading raster: {input_raster_path}")

    # Read raster to NumPy array
    ras = Raster(input_raster_path)
    arr = arcpy.RasterToNumPyArray(ras, nodata_to_value=np.nan)
    arr = arr.astype(np.float64)

    print(f"  Shape     : {arr.shape}")
    print(f"  Raw range : min={np.nanmin(arr):.8f}, max={np.nanmax(arr):.8f}")

    # Z-Split normalization
    result = np.zeros_like(arr)

    # Positive half → [0, 1]
    pos_mask = arr > 0
    if pos_mask.any():
        max_pos = np.nanmax(arr[pos_mask])
        if max_pos != 0:
            result[pos_mask] = arr[pos_mask] / max_pos

    # Negative half → [-1, 0]
    neg_mask = arr < 0
    if neg_mask.any():
        min_neg = np.nanmin(arr[neg_mask])
        if min_neg != 0:
            result[neg_mask] = arr[neg_mask] / abs(min_neg)

    # Restore NaN for nodata pixels
    result[np.isnan(arr)] = np.nan

    print(f"  Z-Split range : min={np.nanmin(result):.4f}, max={np.nanmax(result):.4f}")

    # Get spatial reference info from original raster
    lower_left = arcpy.Point(ras.extent.XMin, ras.extent.YMin)
    cell_size  = ras.meanCellWidth
    sr         = ras.spatialReference

    # Convert NumPy array back to raster
    out_ras = arcpy.NumPyArrayToRaster(
        result,
        lower_left_corner=lower_left,
        x_cell_size=cell_size,
        value_to_nodata=np.nan
    )

    # Assign spatial reference
    arcpy.management.DefineProjection(out_ras, sr)

    # Save
    out_ras.save(output_raster_path)
    print(f"  Saved: {output_raster_path}")

    return output_raster_path


# =============================================================================
# MAIN
# =============================================================================

if __name__ == "__main__":

    print("=" * 60)
    print("Z-Split Normalization — ArcGIS Pro")
    print("Author: Abdulrhman Almoadi (KACST)")
    print("=" * 60)

    if not arcpy.Exists(INPUT_RASTER):
        raise FileNotFoundError(f"Input raster not found:\n  {INPUT_RASTER}")

    zsplit_normalize_arcpy(INPUT_RASTER, OUTPUT_RASTER)

    print("\nDone. Z-Split normalization complete.")
    print(f"Output: {OUTPUT_RASTER}")
