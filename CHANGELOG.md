# v1.2.0 Updated normalisation + added channel selection function
- The uint8 conversion can now be done by giving the original bit encoding.
  - By doing so, the image will not be normalised for uint8 (255) format
  - Warning as if chosen wrongly, it can leads to value overflow
- Logic is as before if None is passed as original encoding
- Channels can now be selected
  - It is useful when dealing with satellite images (format as [2,1,0])
  - Fail safe in case images has less than 3 channels.

# v1.1.0 Package is now pip installable
- Added a setup.py to be able to install this program as python package.
- Simply run `pip install git+https://github.com/Adrien-Dorise/tif2png`

# v1.0.0 Added multispectral support

## Multispectral
- It is now possible to convert multi-spectral images
- If an image has >3 bands, the bands are split into three groups. Each group corresponds to the average of its bands.
- If an image has 2 bands, the bands are merged by average into one unique band

## Alpha channel deletion
- An alpha channel automatic detection and deletion is set up.
- The alpha channel is detected by taking the band containing a vast majority of max pixel values.
- If an alpha channel is detected, it is automatically deleted to avoid merging problems with multispectral images.

## Non-linear pixel normalisation
- As TIF images usually havea higher pixel range than PNG/JPG images (uint16 instead of uint8), a normalisation method is set.
- Two options are available:
  - Linear normalisation between [0,255] uint8.
  - Non-linear normalisation between [0,255] uint8 excluding limit values (typically, 1% of min/max).
**Note**: Because of the high range of some TIF images, most of the contrast is lost when normalising to uint8. Moreover, some limit values take up a significant chunk of the range, sometime for a few pixels. The non-linear normalisation takes care of these limit pixels and improve the contrast in some images.

## Added dummy data for testing
- More test data are added.
- These data take care of various cases.
- Example: Grayscale, grayscale+alpha, RGB, multispectral.  

## Added main
- Added main to launch the conversion easily from your farvorite IDE.
- Some parameters to take care of:
  - input and output paths
  - output file format (JPG or PNG)
  - Conversion by file or folder possible
  - Use of the non-linear normalisation (stretch parameter).   

# v0.0.0 - First Commit  
- First commit of this repo.
- Basic conversion already working 
- Basic files (Licence, README...) created