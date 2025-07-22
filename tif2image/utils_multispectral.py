import numpy as np

def average_xs_to_RGB(img):
    """
    Convert a multispectral image into a 3 band RGB image.
    This is done by dividing the bands into three distinct part (R, G and B), 
    and then calculating the average for each part.
    
    Note, that most multispectral information is lost during the process, but it allows for
    a quick visualisation of the original TIF image.

    Args:
        img: (np.array (n, m, channels)): Multispectral image with more than three bands

    Return:
        rgb_img (np.array (n, m, 3)): RGB image.
    """
    
    if(np.shape(img))[-1] == 2:
        print("WARNING: Image contains only two bands. A merge of the bands will be done to fit on a grayscale image.")            
        img = np.mean(img,axis=2)
        img = np.expand_dims(img,-1) 

    norm_per_band = np.shape(img)[-1] // 3
    rgb_img = np.zeros((np.shape(img)[0], np.shape(img)[1], 3))
    
    rgb_img[:,:,0] = np.mean(img[:,:,0:norm_per_band],axis=2)
    rgb_img[:,:,1] = np.mean(img[:,:,norm_per_band+1:norm_per_band*2],axis=2)
    rgb_img[:,:,2] = np.mean(img[:,:,(norm_per_band*2)+1:-1],axis=2)

    print(f"Multispectral image downscaled from {np.shape(img)[-1]} bands to 3 RGB bands")
    return rgb_img


def remove_extra_bands(img):
    if img.ndim != 3:
        raise ValueError(f"Unsupported image shape: {img.shape}")

    num_bands = img.shape[2]

    # Determine how to build a 3-channel RGB image
    if num_bands == 1:
        # Grayscale ? replicate across 3 channels
        img = np.repeat(img, 3, axis=2)

    elif num_bands == 2:
        # Use band 1 as grayscale RGB (ignore band 2: probably alpha or mask)
        img = np.repeat(img[0:1], 3, axis=2)

    elif num_bands >= 3:
        # Use specified RGB band indices or default to (2, 1, 0)
        img = img[:, :, :3]
        indices = (2,0,1)  # default: assumes BGR to RGB
        img = np.stack([img[:,:,i] for i in indices], axis=2)

    else:
        raise ValueError(f"Unsupported number of bands: {num_bands}")
    
    return img