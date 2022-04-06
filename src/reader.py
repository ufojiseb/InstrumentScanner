from PIL import Image
from typing import Tuple
from os.path import join, isdir, isfile
import os

from src.cropper import crop
from src.ocr import OCR
from src.logger import Logger


def correct_group_name(group_name: str) -> str:
	# ensures that there aren't illegal characters in the group_name
	
	chars = []
	for c in group_name:
		if c.isalpha() or c.isdigit() or c in " .,-&()":
			chars.append(c)
		elif c == "\n":
			chars.append(" ")

	return "".join(chars).strip()


def rename_groups(images_dir: str, crop_page: int, top_left_corner: Tuple[int, int], bottom_right_corner: Tuple[int, int]) -> None:
	
	groups_paths = [join(images_dir, d) for d in os.listdir(images_dir) if isdir( join(images_dir, d) )]

	for d in groups_paths:
		# a list of all the files in each subdirectory
		files = [join(d, f) for f in os.listdir(d) if isfile( join(d, f) )]
		
		img = Image.open( files[crop_page] )
		cropped = crop(img, top_left_corner, bottom_right_corner)

		group_name = correct_group_name( OCR.read(cropped) )
		group_name = join(images_dir, group_name)

		try:
			os.rename(d, group_name)
			Logger.log(f'Renamed "{d}" >>> "{group_name}"')
		except (OSError, FileExistsError):  #On linux it raises OSError instead of FileExistsError
			Logger.error(f'Could not rename "{d}" >>> "{group_name}" (directory already exists)')
		except FileNotFoundError:
			Logger.error(f'Could not rename "{d}" >>> "{group_name}" (origin directory not found)')
