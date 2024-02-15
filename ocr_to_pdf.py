import pytesseract
from pdf2image import convert_from_path
import glob

pdfs = glob.glob(r"cgm/*.pdf")

for pdf_path in pdfs:
    pages = convert_from_path(pdf_path, 500)

    text = ""
    for pageNum,imgBlob in enumerate(pages):
        text += pytesseract.image_to_string(imgBlob,lang='eng')

    with open(f'{pdf_path[:-4]}_text.txt', 'w') as the_file:
        the_file.write(text)
