from PIL import Image
import numpy as np

from src.enhancer import enhance
from src.pdf_converter import load_pages


class Superimposer:
	def __init__(self) -> None:
		self.images = []

	def add(self, pdf_path: str) -> None:
		# adds the first page of a pdf to the superimposed final image
	
		img = load_pages(pdf_path)[0]  # takes only the first page
		self.images.append( enhance(img) )
	
	def superimpose(self) -> Image:
		# creates and returns the superimposed image of all the pdfs passed previously
		
		# 'uint16' is used to avoid overflow when adding arrays
		# (uint8 is the default, which has a range 0-255) 
		base_array = None
		for img in self.images:
			if base_array is None:
				base_array = np.asarray(img, dtype='uint16')
			else:
				base_array = base_array + np.asarray(img, dtype='uint16')
		
		# if a pixel has a value below 255 * len(self.images) it means that at
		# least one image has a black pixel in that position, resulting in a black
		# pixel in the superimposed image too 
		treshold = 255 * len(self.images)
		base_array = np.where(base_array < treshold, 0, 255)

		# uint8 can be used as max value has been capped to 255 in the previous step
		return Image.fromarray( np.uint8(base_array) )
