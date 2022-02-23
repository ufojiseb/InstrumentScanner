from multiprocessing.connection import Client, Listener
from multiprocessing import Process

import subprocess
from subprocess import Popen, PIPE, DEVNULL, STDOUT

from os.path import join, basename, splitext

from src.logger import Logger


class Splitter:
	N_PROCESSES: int = 4
	
	LISTENER_ADDRESS = 'localhost'
	LISTENER_PORT = 6000

	RESOLUTION = 150

	@staticmethod
	def set_resolution(dpi: int) -> None:
		Splitter.RESOLUTION = dpi
	

	@staticmethod
	def _get_number_of_pages(pdf_path: str) -> int:
		command = ["pdfinfo", pdf_path]

		proc = Popen(command, stdout=PIPE, stderr=PIPE)
		out, err = proc.communicate()

		for line in out.decode("utf8", "ignore").split("\n"):

			try:
				tokens = line.split(":")
				key, value = tokens[0], tokens[1]
			except IndexError:
				continue
			
			if key == "Pages":
				return int(value)

		raise ValueError("Cannot extract number of pages from pdf")


	@staticmethod
	def _execute(id: int, pdf_path: str, out_dir: str, start_page: int, n_pages: int) -> None:
		
		pdf_name = splitext( basename(pdf_path) )[0]  # pdf name without extension
		out_base = join(out_dir, pdf_name)
		end_page = start_page + n_pages

		args = [
			"pdftoppm", 
			"-r", str(Splitter.RESOLUTION), 
			"-png", 
			pdf_path, 
			"-f", str(start_page), 
			"-l", str(end_page), 
			out_base
		]
		subprocess.check_call(args, stdout=DEVNULL, stderr=STDOUT)

		with Client((Splitter.LISTENER_ADDRESS, Splitter.LISTENER_PORT)) as conn:
			conn.send(id)
	
	
	@staticmethod
	def convert(pdf_path: str, out_dir: str) -> None:
		
		tot_pages = Splitter._get_number_of_pages(pdf_path)
		
		n_pages = tot_pages // Splitter.N_PROCESSES
		surplus = tot_pages % Splitter.N_PROCESSES

		with Listener((Splitter.LISTENER_ADDRESS, Splitter.LISTENER_PORT)) as listener:
			already_done = 0
			
			for proc_number in range(Splitter.N_PROCESSES):
				
				if proc_number < surplus:
					proc_n_pages = n_pages + 1
				else:
					proc_n_pages = n_pages
				
				start_page = already_done
				already_done += proc_n_pages

				p = Process(target=Splitter._execute, args=(proc_number, pdf_path, out_dir, start_page, proc_n_pages))
				p.start()
			
			Logger.log("Started processes to convert pages in images...")

			for i in range(Splitter.N_PROCESSES):
				with listener.accept() as conn:
					finished_id = conn.recv()
					Logger.log(f"Process {finished_id} done [{i+1}/{Splitter.N_PROCESSES}]")
