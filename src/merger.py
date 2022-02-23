from typing import List
from PyPDF2 import PdfFileMerger


def merge(pdf_paths: List[str], merged_filepath: str) -> None:
	merger = PdfFileMerger()

	for path in pdf_paths:
		merger.append(path)
	
	merger.write(merged_filepath)
	merger.close()
