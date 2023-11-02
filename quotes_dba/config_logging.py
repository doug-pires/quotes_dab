import logging

# Create the Formatter
formatter = logging.Formatter(
    "%(asctime)s :-: %(levelname)s :-: %(name)s :-: %(message)s"
)


def get_stream_handler() -> logging.StreamHandler:
    """
    Create and configure a logging StreamHandler with a specific formatter and log level.

    Returns:
        logging.StreamHandler: An instance of logging.StreamHandler configured with the specified formatter
            and log level.

    Example:
        ```python
        handler = get_stream_handler()
        logger = logging.getLogger(__name__)
        logger.addHandler(handler)
        logger.setLevel(logging.INFO)
        ```

    This function creates a logging StreamHandler, which directs log messages to the console (stdout).
    It configures the StreamHandler with a predefined formatter and sets the log level to INFO by default.

    Returns the configured StreamHandler, ready to be added to a logger for handling log messages.
    """
    stream_handler = logging.StreamHandler()
    # Add Formatter to Handlers
    stream_handler.setFormatter(formatter)
    stream_handler.setLevel(logging.INFO)
    return stream_handler


# Create Logger and set its level
def get_stream_logger(logger_name: str) -> logging.Logger:
    """
    Create and configure a logging logger with a specific name, log level, and a StreamHandler.

    Args:
        logger_name (str): The name of the logger.

    Returns:
        logging.Logger: A Logger instance configured with the specified name, log level, and a StreamHandler.

    Example:
        ```python3
            logger = get_logger('my_logger')
            logger.info('This is an informational message')
            logger.error('This is an error message')
        ```
    """
    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.INFO)
    # Add the Handlers to Logger
    logger.addHandler(get_stream_handler())
    return logger


if __name__ == "__main__":  # pragma: no cover
    # Testing
    logger = get_stream_logger("app_logger")
    logger.info("Hi from Logging!")
