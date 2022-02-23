from typing import Literal, Dict
from os.path import join, isfile, isdir, basename
import os

from fpdf import FPDF

from src.logger import Logger


class PDF_Writer:
	MARGINS: Dict[str, int] = {
		"top":		0,
		"bottom":	0,
		"left":		0,
		"right":	0,
	}

	UNITS: str = "mm"

	@staticmethod
	def set_margins(top, bottom, left, right) -> None:
		PDF_Writer.MARGIN["top"]	= top
		PDF_Writer.MARGIN["bottom"]	= bottom
		PDF_Writer.MARGIN["left"]	= left
		PDF_Writer.MARGIN["right"]	= right

	
	@staticmethod
	def create_pdfs(images_dir: str, pdf_dir: str, paper_format: Literal[2]) -> None:
		
		if paper_format == "A5":
			orientation = "L"
			paper_width, paper_heigth = 210, 148
		elif paper_format == "A4":
			orientation = "P"
			paper_width, paper_heigth = 210, 297
		elif paper_format == "A3":
			orientation = "L"
			paper_width, paper_heigth = 420, 297
		else:
			raise ValueError(f"Paper format [{paper_format}] not supported")

		m = PDF_Writer.MARGINS
		top, bottom, left, right = m["top"], m["bottom"], m["left"], m["right"]

		coord_x, coord_y = left, top
		img_width = paper_width - (left + right)
		img_heigth = paper_heigth - (top + bottom)

		groups = [join(images_dir, d) for d in os.listdir(images_dir) if isdir( join(images_dir, d) )]
		for group_name in groups:
			
			pdf = FPDF(orientation, PDF_Writer.UNITS, paper_format)
			files = [join(group_name, f) for f in os.listdir(group_name) if isfile( join(group_name, f) )]
			
			for image in files:
				pdf.add_page(orientation)
				pdf.image(image, coord_x, coord_y, img_width, img_heigth)
			
			pdf_name = basename(group_name) + ".pdf"
			pdf_path = join(pdf_dir, pdf_name)

			Logger.log(f'Creating "{pdf_path}"')
			pdf.output(pdf_path, "F")
