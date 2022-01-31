from typing import Tuple
import json


class Config:
	
	SCORES_DIRECTORY: str = ""
	TOP_LEFT_CORNER: Tuple[int, int] = (0, 0)		# (x, y) coordinates of top left corner
	BOTTOM_RIGHT_CORNER: Tuple[int, int] = (0, 0)	# (x, y) coordinates of bottom right corner
	
	@staticmethod
	def load(config_path: str) -> None:
		config = json.load( open(config_path, "r", encoding="utf-8") )

		Config.SCORES_DIRECTORY = 		config["scores_directory"]
		Config.TOP_LEFT_CORNER = 		tuple( config["top_left_corner"] )
		Config.BOTTOM_RIGHT_CORNER = 	tuple( config["bottom_right_corner"] )
