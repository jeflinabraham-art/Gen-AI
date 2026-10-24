import logging


def get_logger(name: str = __name__):
    """
    Creates and returns a logger.
    """

    logging.basicConfig(
        # Show INFO messages and anything more severe, but filter out DEBUG messages.
        level=logging.INFO,

        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )

    return logging.getLogger(name)


# Severity levels (low to high):

# DEBUG: Very detailed information
# INFO: Normal progress
# WARNING: Something unexpected
# ERROR: Something failed
# CRITICAL: A severe failure