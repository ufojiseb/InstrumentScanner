import logging
from logging import Logger
from typing import Literal


class Logger():
	logger: Logger = None
	
	@staticmethod
	def init_logger(logging_format: str = None, logging_level: Literal[20] = logging.INFO) -> None:

		if logging_format is None:
			#logging_format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
			logging_format = '%(message)s'

		logging.basicConfig(format=logging_format, level=logging_level)
		Logger.logger = logging.getLogger(__name__)

	@staticmethod
	def log(msg: str) -> None:
		Logger.logger.info(msg)
	
	@staticmethod
	def error(msg: str) -> None:
		Logger.logger.error(msg)
