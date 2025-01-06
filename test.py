import src.tif2image as tif2image


if __name__ == "__main__":
    from enum import Enum
    class Test(Enum):
        ALL = 0
        TIF2PNG = 1
        TIF2JPG = 2      
    
    test = Test.TIF2JPG
    
    if test in {Test.TIF2JPG, Test.ALL}:
        tif2image.convert_tif_to_image("data_dummy/sample/sample.tif", "data_dummy/output/output.jpg")
    if test in {Test.TIF2PNG, Test.ALL}:
        tif2image.convert_tif_to_image("data_dummy/sample/sample.tif", "data_dummy/output/output.png")

    