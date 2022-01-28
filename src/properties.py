from typing import Tuple
import json


class Properties:
	
	TESSERACT_PATH: str = ""
	SCORES_DIRECTORY: str = ""
	TOP_LEFT_CORNER: Tuple[int, int] = (0, 0)		# (x, y) coordinates of top left corner
	BOTTOM_RIGHT_CORNER: Tuple[int, int] = (0, 0)	# (x, y) coordinates of bottom right corner
	
	@staticmethod
	def load(properties_path: str) -> None:
		properties = json.load( open(properties_path, "r", encoding="utf-8") )

		Properties.TESSERACT_PATH = 		properties["tesseract_path"]
		Properties.SCORES_DIRECTORY = 		properties["scores_directory"]

		Properties.TOP_LEFT_CORNER = 		tuple( properties["top_left_corner"] )
		Properties.BOTTOM_RIGHT_CORNER = 	tuple( properties["bottom_right_corner"] )
