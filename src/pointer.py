from distutils.log import Log
from PIL import Image
from typing import List, Tuple

from src.logger import Logger


def find_coordinates(image: str, pixel_color: Tuple[int, int, int], default_top_left_corner: Tuple[int, int], default_bottom_right_corner: Tuple[int, int]) -> List[ Tuple[int, int] ]:
	try:
		img = Image.open(image)
	except FileNotFoundError:
		Logger.error("Could not open superimposed image! Using default coordinates")
		return [default_top_left_corner, default_bottom_right_corner]

	img = img.convert("RGB")
	width, heigth = img.size
	coordinates = []

	Logger.log(f"Finding points in the superimposed image...")

	for x in range(width):
		for y in range(heigth):

			if img.getpixel((x, y)) == pixel_color:
				coordinates.append((x, y))

				if len(coordinates) == 2:
					return coordinates

	length = len(coordinates)
	if length < 2:
		raise ValueError(f"Could not find enough points ({length}) in the superimposed image")
	elif length > 2:
		raise ValueError(f"Found too many points ({length}) in the superimposed image")
