import argparse
import matplotlib.pyplot as plt
import os
import rasterio
import numpy as np
import cv2
import numpy as np

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
    
    print(f"Multispectral image downscaled from {np.shape(img)[-1]} bands to 3 RGB bands")
    return rgb_img

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

def convert_tif_to_image(input_file, output_file, stretch=False):
    """
    Convert a TIF image to anther image format (PNG, JPG).

    Args:
        input_file (str): Path to the input TIF file.
        output_file (str): Path to the output JPG or PNG file.
        stretch (boolean): True to use a stretching method when normalising the image to int [0,255].
                           Stretching sometimes improves image quality as it eliminates outlier values, at the cost of min/max information
    """
    print(f"INPUT: {input_file}") 
    with rasterio.open(input_file) as src:
        img = src.read()
    
    
    if len(np.shape(img)) >= 3:        
        img = np.moveaxis(img,0, -1)

        alpha_axis = get_alpha_channel(img)
        if alpha_axis > 0: # An alpha channel is detected
            img = np.delete(img,alpha_axis,2)

        if(np.shape(img))[-1] == 2:
            print("WARNING: Image contains only two bands. A merge of the bands will be done to fit on a grayscale image.")            
            img = np.mean(img,axis=2)
            img = np.expand_dims(img,-1) 

        if(np.shape(img))[-1] > 3:
            img = multispectral_to_RGB(img)
    
    if(stretch):
        img = stretch_0_255(img)
    else:
        img = cv2.normalize(img, None, alpha = 0, beta = 255, norm_type = cv2.NORM_MINMAX, dtype = cv2.CV_8U)

    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    cv2.imwrite(output_file, cv2.cvtColor(img.astype('uint8'),cv2.COLOR_BGR2RGB))
    
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
    parser = argparse.ArgumentParser(description="Convert TIF images to image format (PNG, JPG) and visualize them.")
    subparsers = parser.add_subparsers(dest="command")

    # Define the convert command
    convert_parser = subparsers.add_parser("convert", help="Convert a TIF image to image format (PNG, JPG).")
    convert_parser.add_argument("input_file", help="Path to the input TIF file.")
    convert_parser.add_argument("output_file", help="Path to the output image file, with correct extension.")

    # Define the visualize command
    visualize_parser = subparsers.add_parser("visualize", help="Visualize a PNG/JPG image.")
    visualize_parser.add_argument("jpg_file", help="Path to the input PNG/JPG file.")

    # Define the batch convert command
    batch_convert_parser = subparsers.add_parser("batch_convert", help="Convert multiple TIF images to PNG/JPG in batch mode.")
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