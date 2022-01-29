from PIL import Image
import pytesseract


class OCR:
	CONFIG: str = ""
	
	@staticmethod
	def set_tesseract_path(tesseract_path: str) -> None:
		# sets the path where tesseract.exe is on the system, if not in PATH (environment variables)
		pytesseract.pytesseract.tesseract_cmd = tesseract_path
	
	@staticmethod
	def set_config(config: str) -> None:
		OCR.CONFIG = config

	@staticmethod
	def read(image: Image) -> str:
		# returns the text found in the image passed as parameter
		return pytesseract.image_to_string(image, config=OCR.CONFIG)
