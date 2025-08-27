"""Example of how to use Logaroo."""

from logaroo import logger

# Basic logging, everything is ready to go
logger.info("This is a simple log message")
logger.warning("You can use different severity levels")
logger.debug("This isn't shown, because the default log level is INFO")

# Change the log level
logger.level = "debug"
logger.info(f"Changing the log level to {logger.level.upper()}")
logger.debug("Now you can see debug messages")

# Change the log template
logger.template = "{elapsed} {color}{icon} {level:<8} {message}"
logger.info("You can change the log message template")
logger.warning("For example, using elapsed time instead of time stamp")

# Add a log level
logger.add_level("time", 23, "[cyan]", "\N{ALARM CLOCK}")
logger.info("Adding a new log level: TIME")
logger.time("I'm not a standard log level")

# Show all levels
logger.info("During development, you can inspect all available log levels")
logger.log_to_all_levels()
logger.info(f"The log level is still {logger.level.upper()}")
