from PIL import Image
import numpy as np


def enhance(image: Image.Image) -> Image.Image:

	# converts image to greyscale
	image = image.convert('L')

	pixel_array = np.asarray(image)

	# computes the average pixel level
	avg_color_per_row = np.average(pixel_array, axis=0)
	avg_color = np.average(avg_color_per_row, axis=0)
	
	# the threshold under which a pixel will be completely turned black
	treshold = avg_color - avg_color * 0.20

	# Loops through each pixel and checks if its value is below the treshold.
	# If it is then it becomes pure black (0), otherwise it becomes pure white (255)
	pixel_array = np.where(pixel_array < treshold, 0, 255)
	image = Image.fromarray( np.uint8(pixel_array) )

	return image
