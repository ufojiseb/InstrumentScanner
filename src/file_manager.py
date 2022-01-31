from typing import List, Tuple
from os.path import isfile, join
import os


def correct_filename(filename: str) -> str:
	# ensures that there aren't illegal characters in the filename

	# removes the extension from the filename (.pdf) and saves it for later
	extension = filename[-4:]
	filename = filename[:-4]
	
	chars = []
	for c in filename:
		if c.isalpha() or c.isdigit() or c in " .,-&()":
			chars.append(c)
		elif c == "\n":
			chars.append(" ")

	filename = "".join(chars).strip()

	return filename + extension


def get_files_list(path: str) -> List[Tuple[str, str]]:
	# returns a list with a tuple for each pdf file, containing the name of the file and its complete path
	return [(f, join(path, f)) for f in os.listdir(path) if isfile(join(path, f)) and f.endswith('.pdf')]


def rename_file(directory: str, old_name: str, new_name: str) -> None:
	old_file_path = join(directory, old_name)
	new_file_path = join(directory, new_name)

	os.rename(old_file_path, new_file_path)
