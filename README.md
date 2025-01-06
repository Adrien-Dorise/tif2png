**TIF2PNG**
================

Convert TIF images to PNG and visualize them with ease!

**Overview**
------------

`tif2png` is a Python project that provides a simple way to convert TIF (Tagged Image File Format) image files into PNG (Portable Network Graphics) format. Additionally, it allows you to visualize the converted images.

**Features**
----------

* Convert multiple TIF files to PNG with a single command
* Visualize the converted PNG images using matplotlib
* Supports batch processing of TIF files

**Requirements**
-------------

* Python > 3.12
* `matplotlib` library for visualization (optional)
* `pillow`for image management

**Usage**
-----

1. Clone this repository: `git clone https://github.com/your-username/tif2png.git`
2. Install the required libraries: `pip install matplotlib`
3. Run the converter script: `python tif2png.py <input_tif_file> <output_png_file>`
4. Visualize the converted PNG image (optional): `python visualize.py <png_file>`

**Example Use Cases**
--------------------

* Convert a single TIF file to PNG:
```bash
$ python tif2png.py convert input.tif output.png
```
* Visualise an png
```bash
$ python visualize.py output.png
```
* Convert multiple TIF files to PNG in batch mode:
```bash
$ python tif2png.py batch_convert -i input1.tif input2.tif -o output/
```

**License**
-------

This project is licensed under the MIT License. See LICENSE.md for more information.