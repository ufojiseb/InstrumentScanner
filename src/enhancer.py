from PIL import Image
import numpy as np
from os.path import join, isfile
import os

from src.logger import Logger


class Enhancer:
	THRESH_MIN, THRESH_MAX = 0, 0
	THRESHOLD_FACTOR = 0.0
	
	@staticmethod
	def set_equalizer_threshold_range(thresh_min: int, thresh_max: int) -> None:
		Enhancer.THRESH_MIN = thresh_min
		Enhancer.THRESH_MAX = thresh_max
	
	@staticmethod
	def set_threshold(threshold_factor: float) -> None:
		if not (-1 <= threshold_factor <= 1):
				threshold_factor = 0

		Enhancer.THRESHOLD_FACTOR = threshold_factor
	
	@staticmethod
	def enhance_all(images_dir: str, mode: str) -> None:
		# Enhances all the images in the specified directory
		
		Logger.log(f"Enhancing images...")

		# a list of all the files in the specified direcrtory
		files = []
		for f in os.listdir(images_dir):
			file_path = join(images_dir, f)
			
			if isfile(file_path) and file_path.endswith((".jpg", ".jpeg", ".png")):
				files.append(file_path)

		for f in files:
			Enhancer.enhance(f, mode)
	
	@staticmethod
	def enhance(image_path: str, mode: str) -> None:

		image = Image.open(image_path)

		# converts image to greyscale, if not already done
		image = image.convert('L')
		pixel_array = np.asarray(image)

		# computes the average pixel level
		avg_color_per_row = np.average(pixel_array, axis=0)
		avg_color = np.average(avg_color_per_row, axis=0)
		
		# the threshold under which a pixel will be completely turned black
		threshold = avg_color - avg_color * Enhancer.THRESHOLD_FACTOR

		if mode == "equalize":
			#min_i = np.min(pixel_array)
			#max_i = np.max(pixel_array)
			
			min_i = threshold - Enhancer.THRESH_MIN
			max_i = threshold + Enhancer.THRESH_MAX

			min_o, max_o = 0, 255

			# (value-min_i)*(((max_o-min_o)/(max(max_i-min_i, 1)))+min_o)
			equalization_factor = (((max_o-min_o)/(max_i-min_i))+min_o)

			pixel_array = pixel_array - min_i
			pixel_array = pixel_array * equalization_factor

			pixel_array = np.where(pixel_array < min_o, min_o, pixel_array)
			pixel_array = np.where(pixel_array > max_o, max_o, pixel_array)

		elif mode == "extreme":
			# Loops through each pixel and checks if its value is below the treshold.
			# If it is then it becomes pure black (0), otherwise it becomes pure white (255)
			pixel_array = np.where(pixel_array < threshold, 0, 255)


		image = Image.fromarray( np.uint8(pixel_array) )
		image.save(image_path)
