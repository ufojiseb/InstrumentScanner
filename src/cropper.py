from typing import Tuple
from PIL import Image


def crop(image: Image.Image, top_left_coord: Tuple[int, int], bottom_right_coord: Tuple[int, int]) -> Image.Image:
	# crops the image at the specified coordinates

	left = 		top_left_coord[0]
	top = 		top_left_coord[1]
	right = 	bottom_right_coord[0] + 1  # +1 so to include the last row and column
	bottom = 	bottom_right_coord[1] + 1  # +1 so to include the last row and column

	return image.crop((left, top, right, bottom))
