import sys
from typing import List, Tuple

from src.ocr import OCR
from src.cropper import load_and_crop
from src.file_manager import get_files_list, rename_file, correct_filename
from src.config import Config
from src.logger import Logger
from src.superimposer import Superimposer


def superimpose(path_list: List[Tuple[str, str]]) -> None:
	
	sup = Superimposer()
	
	for tup in path_list:
		file_name = tup[0]
		file_path = tup[1]

		Logger.log(f'Adding "{file_path}"')
		sup.add(file_path)
	
	Logger.log(f"Creating superimposed image")
	superimposed = sup.superimpose()
	superimposed.save("superimposed.png")


def read_and_rename(path_list: List[Tuple[str, str]]) -> None:
	for tup in path_list:
		file_name = tup[0]
		file_path = tup[1]
	
		cropped = load_and_crop(file_path, Config.TOP_LEFT_CORNER, Config.BOTTOM_RIGHT_CORNER)

		new_file_name = correct_filename( OCR.read(cropped) + ".pdf" )

		try:
			rename_file(Config.SCORES_DIRECTORY, file_name, new_file_name)
			Logger.log(f'Renamed "{file_name}" >>> "{new_file_name}"')
		except FileExistsError:
			Logger.error(f'Could not rename "{file_name}" >>> "{new_file_name}" (destination file already exists)')
		except FileNotFoundError:
			Logger.error(f'Could not rename "{file_name}" >>> "{new_file_name}" (origin file does not exists)')


def main() -> None:
	Logger.init_logger()

	DEFAULT_MODE = "--rename"
	CONFIG_PATH = "config.json"

	if len(sys.argv) > 1:
		MODE = sys.argv[1]
	else:
		MODE = DEFAULT_MODE

	Config.load(CONFIG_PATH)
	Logger.log(f"Loaded {CONFIG_PATH}")

	path_list = get_files_list(Config.SCORES_DIRECTORY)
	Logger.log(f"Loaded pdf list: {[f[0] for f in path_list]}")

	if MODE == "--superimpose" or MODE == "-s":
		superimpose(path_list)
	elif MODE == "--rename" or MODE == "-r":
		read_and_rename(path_list)
	else:
		err_str =  "Error: invalid argument\n"
		err_str += "Usage: python main.py [mode]\n"
		err_str += "-s --superimpose   to create a superimposed image of all the pdfs\n"
		err_str += "-r --rename        to read the instrument and rename all the pdfs\n"

		Logger.error(err_str)


if __name__ == "__main__":
	main()
