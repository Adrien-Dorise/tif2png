import src.tif2png as tif2png
import src.tif2jpg as tif2jpg


if __name__ == "__main__":
    from enum import Enum
    class Test(Enum):
        ALL = 0
        TIF2PNG = 1
        TIF2JPG = 2      
    
    test = Test.TIF2JPG
    
    if test in {Test.TIF2JPG, Test.ALL}:
        tif2jpg.convert_tif_to_jpg("data_dummy/sample/sample.tif", "data_dummy/output/output.jpg")
    if test in {Test.TIF2PNG, Test.ALL}:
        tif2png.convert_tif_to_png("data_dummy/sample/sample.tif", "data_dummy/output/output.png")

    