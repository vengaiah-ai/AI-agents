import logging
import sys

def setup_logging():
    """
    Configures the logging for the application to ensure output is always visible.
    """
    # Get the root logger
    logger = logging.getLogger()
    logger.setLevel(logging.INFO) # Set the minimum level of messages to log

    # Create a handler to write logs to the console (stdout)
    handler = logging.StreamHandler(sys.stdout)
    
    # Create a formatter to define the log message format
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    handler.setFormatter(formatter)
    
    # Add the handler to the logger
    # This check prevents adding duplicate handlers if the function is called multiple times
    if not logger.handlers:
        logger.addHandler(handler)

