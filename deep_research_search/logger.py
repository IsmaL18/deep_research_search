import logging
import sys

from deep_research_search.config import global_config

# Logger configuration
logger = logging.getLogger("app_logger")
logger.setLevel(getattr(logging, global_config.log_level.upper(), logging.INFO))

# Logs format
log_format = logging.Formatter(
    "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

# Handler in the console (print the logs in the console)
console_handler = logging.StreamHandler(sys.stdout)
console_handler.setLevel(getattr(logging, global_config.log_level.upper(), logging.INFO))
console_handler.setFormatter(log_format)

# Add the handler to the logger
logger.addHandler(console_handler)

