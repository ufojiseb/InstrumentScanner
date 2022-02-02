from PyPDF2 import PdfFileWriter
from PIL.Image import Image
import pdf2image
from typing import List, Literal


def pdf_to_images(pdf_path: str) -> List[Image]:
	# converts the pages of the pdf in a list of images 
	return pdf2image.convert_from_path(pdf_path)
