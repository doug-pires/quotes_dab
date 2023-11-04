from pytest import fixture

from quotes_dab.request_quote import extract_quote


def test_integration_with_api_ninjas(api_key_integration: fixture):
    """
    Test the integration with the Ninjas API using a real API key.

    This integration test verifies that the function 'extract_quote' successfully connects to the
    Ninjas API using the provided real API key and returns a real quote from the API.

    Args:
        api_key_integration (str): A real API key obtained from environment variables.

    Integration Test Steps:
    Given:
    - The REAL API key coming from environment variables.
    - The integration test is running in a CI environment (GitHub Actions).

    When:
    - I call the function 'extract_quote' with the real API key.

    Then:
    - The function should return a list containing at least one dictionary.
    - The 'quote' field in the returned dictionary must be a string.

    This integration test ensures that the 'extract_quote' function works correctly when interacting with
    the Ninjas API and handles the API key properly, especially in a CI environment.

    Note: This integration test is designed to run in a CI environment, such as GitHub Actions,
    where it can safely use a real API key for testing.
    """
    real_api_key = api_key_integration
    real_quote = extract_quote(API_KEY=real_api_key)
    quote = real_quote[0].get("quote")

    # Assertions
    assert isinstance(real_quote, list)
    assert isinstance(quote, str)
