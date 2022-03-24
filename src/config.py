from typing import Literal, Tuple
import json


class Config:
	
	SCORES_DIRECTORY: str = ""
	IMAGES_DIRECTORY: str = ""
	INPUT_PDF_DIRECTORY: str = ""
	SPLITTER_RESOLUTION: int = 150
	GROUP_NUMBER: int = 1
	SUPERIMPOSED_INDEX: int = 1
	ENHANCING_METHOD: str = ""
	THRESHOLD_FACTOR: float = 0
	THRESHOLD_RANGE_MIN: int = 50
	THRESHOLD_RANGE_MAX: int = 50
	PIXEL_COLOR: Tuple[int, int, int] = (0, 0, 0)
	PAPER_FORMAT: Literal[2] = ""
	DEFAULT_TOP_LEFT_CORNER: Tuple[int, int] = (0, 0)		# (x, y) coordinates of top left corner
	DEFAULT_BOTTOM_RIGHT_CORNER: Tuple[int, int] = (0, 0)	# (x, y) coordinates of bottom right corner
	
	@staticmethod
	def load(config_path: str) -> None:
		config:dict = json.load( open(config_path, "r", encoding="utf-8") )

		Config.SCORES_DIRECTORY = 		config["scores_directory"]
		Config.IMAGES_DIRECTORY = 		config["images_directory"]
		Config.INPUT_PDF_DIRECTORY = 	config["input_pdf_directory"]
		Config.GROUP_NUMBER =			int(config["group_number"])
		Config.SUPERIMPOSED_INDEX =		int(config["superimposed_index"]) - 1
		Config.ENHANCING_METHOD =		config["enhancing_method"]
		Config.THRESHOLD_FACTOR =		float(config["threshold_factor"])
		Config.THRESHOLD_RANGE_MIN =	int(config["threshold_range_min"])
		Config.THRESHOLD_RANGE_MAX =	int(config["threshold_range_max"])
		Config.PIXEL_COLOR =			tuple(config["pixel_color"])
		Config.PAPER_FORMAT =			config["paper_format"]
		Config.DEFAULT_TOP_LEFT_CORNER = 		tuple( config["default_top_left_corner"] )
		Config.DEFAULT_BOTTOM_RIGHT_CORNER = 	tuple( config["default_bottom_right_corner"] )
