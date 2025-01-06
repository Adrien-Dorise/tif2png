import argparse
import matplotlib.pyplot as plt
import os
from PIL import Image

# Increase max image size as TIF files can be too big to be opened with standard PIL parameter
Image.MAX_IMAGE_PIXELS = 1000000000

def convert_tif_to_png(input_file, output_file):
    """
    Convert a TIF image to png format.

    Args:
        input_file (str): Path to the input TIF file.
        output_file (str): Path to the output PNG file.
    """
    img = Image.open(rf'{input_file}')
    img = img.convert('RGB')
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    img.save(output_file, "PNG")
    print("TIF image successfully converted:")
    print(f"INPUT: {input_file}") 
    print(f"OUTPUT: {output_file}")

def visualize_png(png_file):
    """
    Visualize a PNG image using matplotlib.

    Args:
        png_file (str): Path to the input PNG file.
    """
    img = plt.imread(rf'{png_file}')
    plt.imshow(img)
    plt.show()

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

    # Define the batch convert command
    batch_convert_parser = subparsers.add_parser("batch_convert", help="Convert multiple TIF images to PNG in batch mode.")
    batch_convert_parser.add_argument("-i", "--input_files", nargs="+", help="Paths to the input TIF files.")
    batch_convert_parser.add_argument("-o", "--output_dir", help="Path to the output directory.")

    args = parser.parse_args()

    if args.command == "convert":
        convert_tif_to_png(args.input_file, args.output_file)
    elif args.command == "visualize":
        visualize_png(args.png_file)
    elif args.command == "batch_convert":
        for input_file in args.input_files:
            output_file = os.path.join(args.output_dir, os.path.basename(input_file).replace(".tif", ".png"))
            convert_tif_to_png(input_file, output_file)

if __name__ == "__main__":
    main()