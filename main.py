import sys

from src.ocr import OCR
from src.cropper import load_and_crop
from src.file_manager import get_files_list, rename_file, correct_filename
from src.config import Config
from src.logger import Logger


def main() -> None:

	Logger.init_logger()

	if len(sys.argv) > 1:
		CONFIG_PATH = sys.argv[1]
	else:
		CONFIG_PATH = "config.json"

	Config.load(CONFIG_PATH)
	Logger.log(f"Loaded {CONFIG_PATH}")

	path_list = get_files_list(Config.SCORES_DIRECTORY)
	Logger.log(f"Loaded pdf list: {[f[0] for f in path_list]}")

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

if __name__ == "__main__":
	main()
