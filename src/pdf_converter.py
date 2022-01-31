import pdf2image
from typing import List


def load_pages(pdf_path: str) -> List:
	# converts the pages of the pdf in a list of images 
	return pdf2image.convert_from_path(pdf_path)
