from setuptools import setup

setup(name="tif2png",
      version="1.1.0",
      description="Convert TIF images to PNG or JPG and visualize them with ease!",
      author="Adrien Dorise",
      author_email="adrien.dorise@hotmail.com",
      url="https://github.com/Adrien-Dorise/tif2png",
      packages=["tif2png.tif",
                ],
      install_requires=[
            "numpy == 1.24.2",
            "opencv-python >= 4.10.0.84",
            "rasterio >= 1.4.3",
      ], 
     )