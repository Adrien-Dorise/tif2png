import argparse
import matplotlib.pyplot as plt
import os
from PIL import Image

# Increase max image size as TIF files can be too big to be opened with standard PIL parameter
Image.MAX_IMAGE_PIXELS = 1000000000

def convert_tif_to_jpg(input_file, output_file):
    """
    Convert a TIF image to jpg format.

    Args:
        input_file (str): Path to the input TIF file.
        output_file (str): Path to the output JPG file.
    """
    img = Image.open(input_file)
    img = img.convert('RGB')
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    img.save(output_file, "JPEG")
    print("TIF image successfully converted:")
    print(f"INPUT: {input_file}") 
    print(f"OUTPUT: {output_file}")

def visualize_jpg(jpg_file):
    """
    Visualize a JPG image using matplotlib.

    Args:
        jpg_file (str): Path to the input JPG file.
    """
    img = plt.imread(jpg_file)
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
        convert_tif_to_jpg(args.input_file, args.output_file)
    elif args.command == "visualize":
        visualize_jpg(args.jpg_file)
    elif args.command == "batch_convert":
        for input_file in args.input_files:
            output_file = os.path.join(args.output_dir, os.path.basename(input_file).replace(".tif", ".jpg"))
            convert_tif_to_jpg(input_file, output_file)

if __name__ == "__main__":
    main()