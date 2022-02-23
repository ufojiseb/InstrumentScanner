from distutils.log import Log
from PIL import Image
from typing import List, Tuple

from src.logger import Logger


def find_coordinates(image: str, pixel_color: Tuple[int, int, int]) -> List[ Tuple[int, int] ]:
	img = Image.open(image)
	img = img.convert("RGB")

	Logger.log(f"Finding points in the superimposed image...")

	coordinates = []

	width, heigth = img.size
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
