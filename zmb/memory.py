import logging
import os

def setup_memory():
    """Configures the logging system."""
    log_file = 'zmb.log'
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler()
        ]
    )
    return logging.getLogger('ZMB_MEMORY')
