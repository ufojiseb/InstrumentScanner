from os.path import join, isfile
import os
import sys

from src.config import Config
from src.logger import Logger
from src.merger import merge
from src.splitter import Splitter
from src.enhancer import Enhancer
from src.grouper import group
from src.superimposer import Superimposer
from src.pointer import find_coordinates
from src.reader import rename_groups
from src.pdf_writer import PDF_Writer


def main() -> None:
	Config.load("config.json")
	Logger.init_logger()


	invalid_parameters_flag = False
	
	if len(sys.argv) > 1:
		options = sys.argv[1]
		available_options = ["s", "x", "r"]  # split, superimpose, rename
		
		options = options[1:]

		if len(options) == 0:
			invalid_parameters_flag = True

		for ch in options:
			if ch not in available_options:
				invalid_parameters_flag = True
	else:
		invalid_parameters_flag = True
	

	if invalid_parameters_flag:
		err_str =  "Error: invalid argument\n"
		err_str += "Usage: python main.py -[mode]\n"
		err_str += "-s (split)          to separate the pdf pages in groups\n"
		err_str += "-x (superimpose)    to create a superimposed image of all the pdfs\n"
		err_str += "-r (rename)         to read the instrument and rename all the pdfs\n"

		Logger.error(err_str)
		exit(-1)

	
	if "s" in options:
		# Searches all the pdf in the input directory and takes only the first one
		in_dir = Config.INPUT_PDF_DIRECTORY

		pdf_paths = [ join(in_dir, f) for f in os.listdir(in_dir) if isfile( join(in_dir, f) ) and f.endswith(".pdf") ]
		
		pdf_name = join(Config.INPUT_PDF_DIRECTORY, "merged.pdf")
		merge(pdf_paths, pdf_name)

		Splitter.set_resolution(Config.SPLITTER_RESOLUTION)
		Splitter.convert(pdf_name, Config.IMAGES_DIRECTORY)

		Enhancer.set_threshold(Config.THRESHOLD_FACTOR)
		Enhancer.set_equalizer_threshold_range(Config.THRESHOLD_RANGE_MIN, Config.THRESHOLD_RANGE_MAX)
		Enhancer.enhance_all(Config.IMAGES_DIRECTORY, Config.ENHANCING_METHOD)

		group(Config.IMAGES_DIRECTORY, Config.GROUP_NUMBER)

	if "x" in options:
		sup = Superimposer()
		sup.add_groups(Config.IMAGES_DIRECTORY, Config.SUPERIMPOSED_INDEX)
		img = sup.superimpose()
		img.save("superimposed.png")

	if "r" in options:
		coords = find_coordinates("superimposed.png", Config.PIXEL_COLOR)

		#rename_groups(Config.IMAGES_DIRECTORY, Config.SUPERIMPOSED_INDEX, Config.TOP_LEFT_CORNER, Config.BOTTOM_RIGHT_CORNER)
		rename_groups(Config.IMAGES_DIRECTORY, Config.SUPERIMPOSED_INDEX, coords[0], coords[1])

		PDF_Writer.create_pdfs(Config.IMAGES_DIRECTORY, Config.SCORES_DIRECTORY, Config.PAPER_FORMAT)


if __name__ == "__main__":
	main()
