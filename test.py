import tif2image.convert as tif2image


if __name__ == "__main__":
    from enum import Enum
    class Test(Enum):
        ALL = 0
        TIF2PNG = 1
        TIF2JPG = 2      
    
    test = Test.TIF2PNG
    
    if test in {Test.TIF2JPG, Test.ALL}:
        tif2image.convert_tif_to_image(r"data_dummy/sample/rgb_sentinel2.tif", r"data_dummy/test/output.jpg")
    if test in {Test.TIF2PNG, Test.ALL}:
        tif2image.convert_tif_to_image(r"data_dummy/sample/rgb_sentinel2.tif", r"data_dummy/test/output.png")

    