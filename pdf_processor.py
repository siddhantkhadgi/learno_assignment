import pdf2image
import pytesseract
from PIL import Image
from typing import List

def find_page_number(pdf_path: str):
    # first get pdf images
    images = process_pdf(pdf_path)
    
    for idx, img in enumerate(images):
        bw_image = img.convert('L')
        
        width, height = bw_image.size
        bottom_middle = bw_image.crop((width // 3, height - 180, 2 * width // 3, height))
    
        text = pytesseract.image_to_string(bottom_middle, config='--psm 6')
        number = ''.join(filter(str.isdigit, text))
        
        if number:
            print(f'index is {idx} and the page number is {number}')
            return idx - (int(number, 10) - 1)
            # return -1
            # return {idx, number}
        
    return -1
    

def process_pdf(pdf_path: str, dpi=200, fmt="jpeg") -> List[Image.Image]:
    return pdf2image.convert_from_path(pdf_path, dpi=200, fmt='jpeg')
    
file_path = 'inputPDF.pdf'
page_idx = find_page_number(file_path)
print(f'index of first page is {page_idx}')