import os
from enum import Enum

import src.tif2image as tif2image

if __name__ == "__main__":
    class Format(Enum):
        ALL = 0
        PNG = 1
        JPG = 2      

    format = Format.JPG
    input_path = "data_dummy/sample"
    
    tif_paths = []
    if input_path.endswith('.tif'):
        tif_paths.append(input_path)
    else:
        for file in os.listdir(rf"{input_path}"):
            if file.endswith('.tif'):
                tif_paths.append(f"{input_path}/{file}")

    if(len(tif_paths)<=0):
        print(f"WARNING: No TIF files found with given path:\n{input_path}")
        exit

    for tif_path in tif_paths:
        if format in {Format.JPG, Format.ALL}:
            tif2image.convert_tif_to_image(tif_path, tif_path[:-3] + "jpg")
        if format in {Format.PNG, Format.ALL}:
            tif2image.convert_tif_to_image(tif_path, tif_path[:-3] + "png")
