from PIL import Image
import pytesseract


class OCR:
	@staticmethod
	def initialize(tesseract_path: str or None) -> None:
		# tesseract_path is where tesseract.exe is on the system, if not in PATH
		if tesseract_path is not None:
			pytesseract.pytesseract.tesseract_cmd = tesseract_path

	@staticmethod
	def read(image: Image) -> str:
		# returns the text found in the image passed as parameter
		return pytesseract.image_to_string(image)
