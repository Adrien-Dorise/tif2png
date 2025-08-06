import argparse
import matplotlib.pyplot as plt
import os
import rasterio
import numpy as np
from PIL import Image
import cv2

import tif2image.utils_multispectral as multispectral
import tif2image.utils_format as format

def get_alpha_channel(image):
    """Get the alpha channel axis in an image.
    The alpha channel is detected as the channel containing the most and a majority of the max pixel value.
    If no channel contains enough max values, -1 is returned.

    Args:
        image (np.array (n,m,channels)): Image with an alpha channel

    Returns:
        alpha_channel (int): Alpha channel axis in the image. -1 if no alpha channel is detected
    """
    
    pixel_count = np.shape(image)[0] * np.shape(image)[1]
    max_value = np.max(image)

    band_count = []
    for band in range(np.shape(image)[-1]):
        band_count.append(np.count_nonzero(image[:,:,band] >= max_value))
    
    alpha_channel = np.where(band_count == np.max(band_count))[0][0] if max(band_count) > pixel_count*0.8 else -1
    
    return alpha_channel


def convert_tif_to_image(input_file, output_file, original_bit_encoding=None, channels_indices=[0,1,2], stretch=False):
    """
    Convert a multi-band TIF image to a standard image format (e.g., PNG or JPG), 
    optionally selecting and reordering channels and applying normalization or contrast stretching.

    Parameters:
    ----------
    input_file : str
        Path to the input GeoTIFF (.tif) file containing the multi-band image.
    output_file : str
        Path to the output image file (e.g., .png, .jpg). 
        The image format is inferred from the file extension.
    original_bit_encoding : int or None, optional (default=None)
        Bit depth used to normalize the input image values.
        For example, if the image is encoded on 12 bits, use 4096 (2^12).
        If None, MinMax bit normalization is applied.
    channels_indices : list of int, optional (default=[0,1,2])
        List of band indices (0-based) to extract from the input image.
        For example, [2,1,0] corresponds to R=band3, G=band2, B=band1 (common for satellite RGB composites).
        If the input image has fewer than 3 bands, all available bands are used.
    stretch : bool, optional (default=False)
        Whether to apply contrast stretching (e.g., min-max normalization excluding outliers).
        This enhances visual contrast but may alter pixel intensity ranges.
    Notes:
    -----
    - Removes alpha channels if detected (based on `get_alpha_channel()` logic).
    - The image is saved using PIL and must be in uint8 format.
    - Supports grayscale or RGB images.
    - For RGB, output shape must be (H, W, 3). For grayscale, (H, W).

    Raises:
    ------
    ValueError if input image bands are incompatible with requested channel selection.
    """
    with rasterio.open(input_file) as src:
        img = []
        if src.meta["count"] < 3:
            channels_indices = list(range(0,src.meta["count"]))
        for c in channels_indices:
            img.append(src.read(c+1))
        img = np.array(img)
        img = np.moveaxis(img,0, -1)

    alpha_axis = get_alpha_channel(img)
    if alpha_axis > 0: # An alpha channel is detected
        img = np.delete(img,alpha_axis,2)

    if original_bit_encoding is not None:
        img = img / original_bit_encoding
        img *= 255
        if np.max(img) > 254:
            print(f"WARNING in tif2png: The maximum bit value after applying original bit encoding conversion is {np.max(img)} > 254. \
                    \nVerify that the image is indeed encoding on {original_bit_encoding}bits")
        img = img.astype(np.uint8)
    else:
        img = cv2.normalize(img, None, alpha = 0, beta = 255, norm_type = cv2.NORM_MINMAX, dtype = cv2.CV_8U)


    if(stretch):
        img = format.stretch_0_255(img)
    
    if img.shape[-1] == 1:
        img = img.reshape(img.shape[0],img.shape[1])
    
    img_pil = Image.fromarray(img)
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    img_pil.save(output_file)
    


def visualize_image(image_file):
    """
    Visualize a JPG or PNG image using matplotlib.

    Args:
        image_file (str): Path to the input image file.
    """
    img = plt.imread(rf'{image_file}')
    plt.imshow(img)
    plt.show()

def process_folder(input_dir, output_dir,original_bit_encoding=None,channels_indices=[0,1,2],stretch=False):
    """
    Convert a an entire folder composed of TIF images to a standard image format (e.g., PNG or JPG), 
    optionally selecting and reordering channels and applying normalization or contrast stretching.

    Parameters:
    ----------
    input_file : str
        Path to the input GeoTIFF (.tif) file containing the multi-band image.
    output_file : str
        Path to the output image file (e.g., .png, .jpg). 
        The image format is inferred from the file extension.
    original_bit_encoding : int or None, optional (default=None)
        Bit depth used to normalize the input image values.
        For example, if the image is encoded on 12 bits, use 4096 (2^12).
        If None, MinMax bit normalization is applied.
    channels_indices : list of int, optional (default=[0,1,2])
        List of band indices (0-based) to extract from the input image.
        For example, [2,1,0] corresponds to R=band3, G=band2, B=band1 (common for satellite RGB composites).
        If the input image has fewer than 3 bands, all available bands are used.
    stretch : bool, optional (default=False)
        Whether to apply contrast stretching (e.g., min-max normalization excluding outliers).
        This enhances visual contrast but may alter pixel intensity ranges.

    """
    print(f"Creating png: {input_dir} -> {output_dir}")
    os.makedirs(output_dir, exist_ok=True)
    for file_name in os.listdir(input_dir):
        if file_name.lower().endswith(".tif"):
            input_path = os.path.join(input_dir, file_name)
            output_path = os.path.join(output_dir, file_name.replace(".tif", ".png"))
            convert_tif_to_image(input_path, output_path,original_bit_encoding,channels_indices,stretch)


def main():
    parser = argparse.ArgumentParser(description="Convert TIF images to PNG and visualize them.")
    subparsers = parser.add_subparsers(dest="command")

    # Define the convert command
    convert_parser = subparsers.add_parser("convert", help="Convert a TIF image to PNG.")
    convert_parser.add_argument("input_file", help="Path to the input TIF file.")
    convert_parser.add_argument("output_file", help="Path to the output PNG file.")

    # Define the visualize command
    visualize_parser = subparsers.add_parser("visualize", help="Visualize a PNG image.")
    visualize_parser.add_argument("png_file", help="Path to the input PNG file.")
  
    # Define the folder convert command
    folder_convert_parser = subparsers.add_parser("folder_convert", help="Convert all TIF images in a folder.")
    folder_convert_parser.add_argument("-i", "--input_dir", help="Directory with TIF images.")
    folder_convert_parser.add_argument("-o", "--output_dir", help="Directory to save PNG images.")

    args = parser.parse_args()

    if args.command == "convert":
        convert_tif_to_image(args.input_file, args.output_file)
    elif args.command == "visualize":
        visualize_image(args.png_file)
    elif args.command == "folder_convert":  
        process_folder(args.input_dir, args.output_dir)

if __name__ == "__main__":
    main()
