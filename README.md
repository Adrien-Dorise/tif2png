**TIF2PNG**
================

Convert TIF images to PNG or JPG and visualize them with ease!

**Overview**
------------

`tif2png` is a Python project that provides a simple way to convert TIF (Tagged Image File Format) image files into PNG (Portable Network Graphics) format. Additionally, it allows you to visualize the converted images.

**Features**
----------

* Convert multiple TIF files to PNG with a single command
* Visualize the converted PNG images using matplotlib
* Convert all TIF files in a folder
* Supports batch processing of TIF files

**Requirements**
-------------

* Python > 3.12
* `matplotlib` library for visualization (optional)
* `opencv-python` for image management
* `rasterio` for TIF management
* `pillow`for image management

**Usage**
-----

1. Clone this repository: `git clone https://github.com/your-username/tif2png.git`
2. Install the required libraries: `pip install matplotlib`
3. Run the converter script: `python tif2image/convert.py <input_tif_file> <output_png_file>`
4. Visualize the converted PNG image (optional): `python tif2image/convert.py <png_file>`

**Example Use Cases**
--------------------

* Convert a single TIF file to PNG:
```bash
$ python tif2image/convert.py  convert input.tif output.png
```
* Convert a whole tif folder int png:
```bash
python tif2image/convert.py folder_convert -i path/to/input_folder -o path/to/output_folder
```
* Visualise an png
```bash
$ python tif2image/convert.py  visualize output.png
```

**License**
-------

This project is licensed under the MIT License. See LICENSE.md for more information.