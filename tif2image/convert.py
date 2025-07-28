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


def convert_tif_to_image(input_file, output_file, stretch=False):
    """
    Convert a TIF image to anther image format (PNG, JPG).

    Args:
        input_file (str): Path to the input TIF file.
        output_file (str): Path to the output JPG or PNG file.
        stretch (boolean): True to use a stretching method when normalising the image to int [0,255].
                           Stretching sometimes improves image quality as it eliminates outlier values, at the cost of min/max information
    """
    with rasterio.open(input_file) as src:
        img = src.read()
    
    
    if len(np.shape(img)) >= 3:        
        img = np.moveaxis(img,0, -1)

        alpha_axis = get_alpha_channel(img)
        if alpha_axis > 0: # An alpha channel is detected
            img = np.delete(img,alpha_axis,2)

        img = multispectral.remove_extra_bands(img)
    
    if(stretch):
        img = format.stretch_0_255(img)
    else:
        img = cv2.normalize(img, None, alpha = 0, beta = 255, norm_type = cv2.NORM_MINMAX, dtype = cv2.CV_8U)

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

def process_folder(input_dir, output_dir):
    print(f"Creating png: {input_dir} -> {output_dir}")
    os.makedirs(output_dir, exist_ok=True)
    for file_name in os.listdir(input_dir):
        if file_name.lower().endswith(".tif"):
            input_path = os.path.join(input_dir, file_name)
            output_path = os.path.join(output_dir, file_name.replace(".tif", ".png"))
            convert_tif_to_image(input_path, output_path)


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
