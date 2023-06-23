import pytesseract
from PIL import Image

img = Image.open('Sample_Images/Datacluster_number_plates (1).jpg')

# Specify the language as English and the page segmentation mode as single block
config = ('-l eng --oem 3 --psm 6')

# Pre-process the image (apply thresholding, smoothing, and edge detection)
#img = img.filter(ImageFilter.SHARPEN)
img = img.convert('L')
img = img.filter(ImageFilter.MedianFilter())
img = img.point(lambda x: 255 if x > 200 else 0)

# Run OCR using Pytesseract
text = pytesseract.image_to_string(img, config=config)

print(text)