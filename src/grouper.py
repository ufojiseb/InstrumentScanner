from os.path import join, exists
import os

from src.logger import Logger

def group(images_path: str, pages_per_group: int):
	
	Logger.log(f"Grouping images...")

	files_list = os.listdir(images_path)
	files_list = [join(images_path, filename) for filename in files_list]

	for i, file_path in enumerate(files_list):
		group_number = i // pages_per_group

		basename = os.path.basename(file_path)
		new_dir = join(images_path, str(group_number).zfill(3))
		new_filepath = join(new_dir, basename)

		if not exists(new_dir):
			os.mkdir(new_dir)

		os.rename(file_path, new_filepath)
