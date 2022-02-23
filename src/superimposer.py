from PIL import Image
import numpy as np

from os.path import join, isfile, isdir
import os

from src.logger import Logger

class Superimposer:
	def __init__(self) -> None:
		self.images = []

	def add(self, image_path: str) -> None:
		# Adds the passed image to the superimposed final image.
		# The image has to be in black and white format.

		Logger.log(f'Adding "{image_path}" to superimposed image')

		self.images.append( Image.open(image_path) )
	
	def add_groups(self, images_dir: str, superimposed_index: int) -> None:
		# Adds the images to the superimposed image. Takes all the groups and
		# for each group adds only the image specified by superimposed_index

		# a list of all the folders in the images directory
		groups_paths = [join(images_dir, d) for d in os.listdir(images_dir) if isdir( join(images_dir, d) )]

		for d in groups_paths:
			# a list of all the files in each subdirectory
			files = [join(d, f) for f in os.listdir(d) if isfile( join(d, f) )]
			
			# adds the image specified in config to the superimposed image
			self.add( files[superimposed_index] )
	
	def superimpose(self) -> Image.Image:
		# creates and returns the superimposed image of all the images passed previously
		
		Logger.log(f"Creating superimposed image...")

		# 'uint16' is used to avoid overflow when adding arrays
		# (uint8 is the default, which has a range 0-255) 
		base_array = None
		for img in self.images:
			if base_array is None:
				base_array = np.asarray(img, dtype='uint16')
			else:
				base_array = base_array + np.asarray(img, dtype='uint16')
		
		# if a pixel has a value below 255 * len(self.images) it means that at
		# least one image has a black pixel in that position, resulting in a black
		# pixel in the superimposed image too 
		treshold = 255 * len(self.images)
		base_array = np.where(base_array < treshold, 0, 255)

		# uint8 can be used as max value has been capped to 255 in the previous step
		return Image.fromarray( np.uint8(base_array) )
