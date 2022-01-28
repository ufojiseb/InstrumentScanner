import sys

from src.ocr import OCR
from src.cropper import load_and_crop
from src.file_manager import get_files_list, rename_file
from src.properties import Properties as props


def main() -> None:

	if len(sys.argv) > 1:
		PROPERTIES_PATH = sys.argv[1]
	else:
		PROPERTIES_PATH = "properties.json"

	props.load(PROPERTIES_PATH)

	
	OCR.initialize(props.TESSERACT_PATH)
	path_list = get_files_list(props.SCORES_DIRECTORY)
	
	for tup in path_list:
		file_name = tup[0]
		file_path = tup[1]
	
		cropped = load_and_crop(file_path, props.TOP_LEFT_CORNER, props.BOTTOM_RIGHT_CORNER)

		new_file_name = OCR.read(cropped) + ".pdf"

		rename_file(props.SCORES_DIRECTORY, file_name, new_file_name)


if __name__ == "__main__":
	main()
