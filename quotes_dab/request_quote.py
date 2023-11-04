import json
import random as rd
from datetime import datetime

import requests
from databricks.sdk import WorkspaceClient

from quotes_dab.config_logging import get_stream_logger
from quotes_dab.provide_config import (
    category_list,
    path_landing_quotes_dbx,
    profile_to_authenticate,
)

logger = get_stream_logger(__name__)


def authenticate_databricks() -> WorkspaceClient:
    """
    Authenticate with Databricks using a specified profile.

    This function creates a WorkspaceClient to authenticate with Databricks using the given profile
    """
    w = WorkspaceClient(profile=profile_to_authenticate)
    return w


def get_api_key(workspace: WorkspaceClient) -> str:
    """
    Retrieve an API key from Databricks secrets.

    Args:
        workspace (WorkspaceClient): An instance of the Databricks WorkspaceClient.

    Returns:
        str: The API key retrieved from Databricks secrets.

    Raises:
        KeyError: If the API key is not found in the specified secrets scope.

    Example:
    ```python
    from databricks import WorkspaceClient
    api_key = get_api_key(WorkspaceClient())
    print(f"API Key: {api_key}")
    ```
    """
    # Get API Key
    API_KEY = workspace.dbutils.secrets.get(scope="api_keys", key="ninjas")
    return API_KEY


def pick_random_category(words_of_list: list) -> str:
    """
    Pick a random category from the provided list of words.

    Args:
        words_of_list (list): A list of categories from which a random category will be chosen.

    Returns:
        str: A randomly selected category from the list.

    This function takes a list of categories and selects a random category from the list.
    It returns the chosen category as a string.

    Example:
        category = pick_random_category(["age", "alone", "amazing"])
    """
    return rd.choice(words_of_list)


def extract_quote(API_KEY) -> list[dict]:
    """
    Extract a random quote from an API and return it as a list of dictionaries.

    Args:
        API_KEY (str): The API key for authentication.

    Returns:
        list[dict]: A list of dictionaries containing the extracted quote.

    Raises:
        Exception: Any exception raised during the API request.

    Note:
        This function makes an API request to retrieve a random quote based on a selected category.
    """
    category = pick_random_category(
        category_list
    )  # Assuming category_list is defined elsewhere
    api_url = f"https://api.api-ninjas.com/v1/quotes?category={category}"
    response = requests.get(api_url, headers={"X-Api-Key": API_KEY})

    if response.status_code == requests.codes.ok:
        quote = response.json()
        logger.info("Extracted quote: %s", quote)
        return quote
    else:
        logger.error(
            "Status Code: %s - Reason: %s", response.status_code, response.text
        )


def save_to_storage(
    workspace: WorkspaceClient, path_dbfs: str, data: list[dict]
) -> None:
    """
    Save data as a JSON file to a specified location in Databricks DBFS.

    Args:
        workspace (WorkspaceClient): The Databricks workspace client for interacting with DBFS.
        path_dbfs (str): The destination path in Databricks DBFS.
        data (list[dict]): The data to be saved as a JSON file.

    Returns:
        None

    Raises:
        AttributeError: If there is an issue with the workspace client or file saving.

    Note:
        This function saves the provided data as a JSON file in Databricks DBFS.
    """
    if data is not None:
        json_formatted = json.dumps(data)
        json_datetime = f"{path_dbfs}/data_json_{datetime.now().timestamp()}"
        try:
            workspace.dbutils.fs.put(json_datetime, json_formatted)
            logger.info("Saved to %s", path_dbfs)
        except AttributeError as e:
            logger.error(e)
    else:
        logger.info("Data returned None")


def main():  # pragma: no cover
    w = authenticate_databricks()
    API_KEY = get_api_key(workspace=w)
    quote = extract_quote(API_KEY=API_KEY)
    save_to_storage(workspace=w, path_dbfs=path_landing_quotes_dbx, data=quote)
