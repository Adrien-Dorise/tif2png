import argparse
import matplotlib.pyplot as plt
import os
import rasterio
import numpy as np
import cv2
import numpy as np

def multispectral_to_RGB(img):
    """
    Concert a multispectral image into a 3 band RGB image.
    This is done by taking dividing the bands into three distinct part (R, G and B), 
    and then calculating the average for each part.
    
    Note, that most multispectral information is lost during the process, but it allows for
    a quick visualisation of the original TIF image.

    Args:
        img: (np.array (n, m, channels)): Multispectral image with more than three bands

    Return:
        rgb_img (np.array (n, m, 3)): RGB image.
    """
    norm_per_band = np.shape(img)[-1] // 3
    rgb_img = np.zeros((np.shape(img)[0], np.shape(img)[1], 3))
    rgb_img[:,:,0] = np.mean(img[:,:,0:norm_per_band],axis=2)
    rgb_img[:,:,1] = np.mean(img[:,:,norm_per_band+1:norm_per_band*2],axis=2)
    rgb_img[:,:,2] = np.mean(img[:,:,(norm_per_band*2)+1:-1],axis=2)
    return rgb_img

def convert_tif_to_image(input_file, output_file):
    """
    Convert a TIF image to anther image format (PNG, JPG).

    Args:
        input_file (str): Path to the input TIF file.
        output_file (str): Path to the output JPG or PNG file.
    """
    with rasterio.open(input_file) as src:
        img = src.read()
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    img = np.moveaxis(img,0, -1)
    
    if(np.shape(img))[-1] == 2:
        img = np.mean(img,axis=2) 
    if(np.shape(img))[-1] > 3:
        img = multispectral_to_RGB(img)
    
    cv2.imwrite(output_file, cv2.cvtColor(img.astype('float32'),cv2.COLOR_BGR2RGB))
    print("TIF image successfully converted:")
    print(f"INPUT: {input_file}") 
    print(f"OUTPUT: {output_file}")



def visualize_image(image_file):
    """
    Visualize a JPG or PNG image using matplotlib.

    Args:
        image_file (str): Path to the input image file.
    """
    img = plt.imread(rf'{image_file}')
    plt.imshow(img)
    plt.show()

def main():
    parser = argparse.ArgumentParser(description="Convert TIF images to JPG and visualize them.")
    subparsers = parser.add_subparsers(dest="command")

    # Define the convert command
    convert_parser = subparsers.add_parser("convert", help="Convert a TIF image to JPG.")
    convert_parser.add_argument("input_file", help="Path to the input TIF file.")
    convert_parser.add_argument("output_file", help="Path to the output JPG file.")

    # Define the visualize command
    visualize_parser = subparsers.add_parser("visualize", help="Visualize a JPG image.")
    visualize_parser.add_argument("jpg_file", help="Path to the input JPG file.")

    # Define the batch convert command
    batch_convert_parser = subparsers.add_parser("batch_convert", help="Convert multiple TIF images to JPG in batch mode.")
    batch_convert_parser.add_argument("-i", "--input_files", nargs="+", help="Paths to the input TIF files.")
    batch_convert_parser.add_argument("-o", "--output_dir", help="Path to the output directory.")

    args = parser.parse_args()

    if args.command == "convert":
        convert_tif_to_image(args.input_file, args.output_file)
    elif args.command == "visualize":
        visualize_image(args.jpg_file)
    elif args.command == "batch_convert":
        for input_file in args.input_files:
            output_file = os.path.join(args.output_dir, os.path.basename(input_file).replace(".tif", ".jpg"))
            convert_tif_to_image(input_file, output_file)

if __name__ == "__main__":
    main()