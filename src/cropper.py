from typing import Tuple
from PIL import Image

from src.pdf_manager import pdf_to_images


def load_and_crop(file_path: str, top_left_coord: Tuple[int, int], bottom_right_coord: Tuple[int, int]) -> Image.Image:
	# loads the pages, creates an image from the first page and crops it at the specified coordinates 
	first_page = pdf_to_images(file_path)[0]

	return crop(first_page, top_left_coord, bottom_right_coord)


def crop(image: Image.Image, top_left_coord: Tuple[int, int], bottom_right_coord: Tuple[int, int]) -> Image.Image:
	# crops the image at the specified coordinates

	left = 		top_left_coord[0]
	top = 		top_left_coord[1]
	right = 	bottom_right_coord[0] + 1  # +1 so to include the last row and column
	bottom = 	bottom_right_coord[1] + 1  # +1 so to include the last row and column

	return image.crop((left, top, right, bottom))
