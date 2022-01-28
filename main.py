import sys

from src.ocr import OCR
from src.cropper import load_and_crop
from src.file_manager import get_files_list, rename_file, correct_filename
from src.properties import Properties as props
from src.logger import Logger


def main() -> None:

	Logger.init_logger()

	if len(sys.argv) > 1:
		PROPERTIES_PATH = sys.argv[1]
	else:
		PROPERTIES_PATH = "properties.json"

	props.load(PROPERTIES_PATH)
	Logger.log(f"Loaded {PROPERTIES_PATH}")

	
	OCR.initialize(props.TESSERACT_PATH)
	path_list = get_files_list(props.SCORES_DIRECTORY)
	Logger.log(f"Loaded pdf list: {[f[0] for f in path_list]}")

	for tup in path_list:
		file_name = tup[0]
		file_path = tup[1]
	
		cropped = load_and_crop(file_path, props.TOP_LEFT_CORNER, props.BOTTOM_RIGHT_CORNER)

		new_file_name = correct_filename( OCR.read(cropped) + ".pdf" )

		rename_file(props.SCORES_DIRECTORY, file_name, new_file_name)
		Logger.log(f'Renamed: "{file_name}" >>> "{new_file_name}"')


if __name__ == "__main__":
	main()
