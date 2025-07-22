import numpy as np

def stretch_0_255(img, percentile=1):
    """
    Normalise an image to a int [0,255] range.
    It includes a non-linear processing of the extremum values.
    All the x% min and max values are assigned to 0 and 255 respectively
    
    Args:
        img: (np.array (n, m, channels)): Image to be stretched
        percentile (int): Percentage of the values to be set to 0 or 255. Default to 1%

    Return:
        img: (np.array (n, m, channels)): Stretched image
    """
    min_percentiles, max_percentiles = np.percentile(img, (percentile, 100-percentile))
    img = np.round(((img - min_percentiles)*(255/(max_percentiles - min_percentiles))).clip(0, 255)).astype(np.uint16)
    return img

def normalize_to_uint8(array):
    """Scale input float or uint16 image to uint8 (0,255)"""
    array = array.astype(np.float32)
    if np.isnan(array).any() or np.isinf(array).any():
        print(f"[WARNING] Detected NaN or inf in array")
    # Compute percentiles - Possible to change values
    min_val = np.percentile(array, 0)
    max_val = np.percentile(array, 100)

    # Avoid divide-by-zero
    if max_val - min_val < 1e-5:
        return np.clip(array, 0, 255).astype(np.uint8)  # Already flat ? skip normalization

    # Normalize safely
    norm = (array - min_val) / (max_val - min_val)
    norm = np.clip(norm, 0, 1)
    return (norm * 255).astype(np.uint8)