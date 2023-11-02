from pytest import fixture

from quotes_dba.request_quote import (
    extract_quote,
    pick_random_category,
    save_to_storage,
)


def test_return_one_string_randomly_between_list_of_categories():
    """
    Test the 'pick_random_category' function to ensure it selects a random string from a list of categories.

    Steps:
    1. Given a list of countries in 'country_list'.
    2. When we call the 'pick_random_category' function to select one randomly.
    3. Then it should select one value that is in the 'country_list'.
    4. Additionally, the selected value should be of type 'str'.
    """
    country_list = ["Germany", "Brazil", "Portugal", "India"]

    random_country = pick_random_category(country_list)

    assert random_country in country_list
    assert isinstance(random_country, str)


def test_if_quote_return_string_when_success(
    mocker: fixture, api_key_mock_local: fixture
):
    """
    Test the 'extract_quote' function to ensure it returns a list of quotes when the API request is successful.

    Args:
        mocker (fixture): A Pytest fixture for mocking external dependencies.
        api_key_mock_local (fixture): A fixture representing the API key used for the test.

    Given:
    - The status code of success (200) is simulated in 'mock_response'.
    - The 'mock_response' object is configured to return a list of quotes.

    When:
    - We call the 'extract_quote' function while running locally with 'api_key_mock_local'.

    Then:
    - The result 'quote' should be of type 'list'.
    """
    mock_response = mocker.Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = ["This is a quote"]
    mocker.patch("requests.get", return_value=mock_response)

    api_key = api_key_mock_local

    quote = extract_quote(API_KEY=api_key)

    assert isinstance(quote, list)


def test_log_error_when_function_return_400(
    mocker: fixture, caplog: fixture, api_key_mock_local: fixture
):
    """
    Test the 'extract_quote' function to log an error message when the API request returns a 400 status code.

    Args:
        mocker (fixture): A Pytest fixture for mocking external dependencies.
        caplog (fixture): A fixture for capturing log messages.
        api_key_mock_local (fixture): A fixture representing the API key used for the test.

    Given:
    - The response is mocked to return a 400 status code with the text "Bad Request".

    When:
    - We call the 'extract_quote' function while running locally with 'api_key_mock_local', which generates the wrong status code.

    Then:
    - The log message should be checked to ensure it contains the expected error message, which includes the status code and reason.
    """
    # Given the response returning 400, because we are mocking it
    mock_response = mocker.Mock()
    mock_response.status_code = 400
    mock_response.text = "Bad Request"
    mocker.patch("requests.get", return_value=mock_response)

    api_key = api_key_mock_local

    extract_quote(API_KEY=api_key)

    # Then the log message should be checked
    expected_log_message = (
        f"Status Code: {mock_response.status_code} - Reason: {mock_response.text}"
    )
    assert expected_log_message in caplog.text


def test_if_data_is_none_will_not_save_to_storage_and_let_user_know(
    caplog: fixture, mock_authentication_databricks: fixture
):
    """
    Test the 'save_to_storage' function to ensure that it does not save data to storage when the data is None and logs a message to inform the user.

    Args:
        caplog (fixture): A fixture for capturing log messages.
        mock_authentication_databricks (fixture): A fixture for mocking the 'authenticate_databricks' function.

    Given:
    - The 'data' is set to None.
    - The 'path' is specified as '/mnt/fake/path'.

    When:
    - We call the 'save_to_storage' function with the provided parameters.

    Then:
    - The code should return a log message indicating that the 'data' is None.
    """
    data = None
    path = "/mnt/fake/path"

    w_mock = mock_authentication_databricks

    save_to_storage(workspace=w_mock, data=data, path_dbfs=path)

    expected_log_message = "Data returned None"
    result_log = caplog.text
    assert expected_log_message in result_log
