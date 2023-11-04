import sys

# sys.path.append("quotes_dba")
path = "/Workspace/Users/d.martins@kigroup.de/.bundle/quotes_dab_bundle/dev/files"
sys.path.append(path)

from quotes_dab.config_logging import get_stream_logger

logger = get_stream_logger(__name__)


def dummy_func() -> str:
    """
    A demonstration function for running a simple task using the JBO API 2.0.

    This function serves as an example and should be used within a conditional block: if __name__ == "__main__".

    Returns:
        str: A string indicating the function's execution.

    Example:
        To use this function, you can call it within the main function and run it as the main script.

        if __name__ == "__main__":
            main()
    """
    logger.info("Running the function for demonstration purposes...")
    # print("Running the function for demonstration purposes...")
    return "Dummy"


def main():  # pragma: no cover
    """
    The main function for running the dummy_func as a script.

    Example:
        if __name__ == "__main__":
            main()
    """
    print(dummy_func())


if __name__ == "__main__":
    main()
