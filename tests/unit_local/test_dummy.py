from quotes_dba.dummy import dummy_func


def test_dummy_func():
    """
    Test the dummy_func function.

    Given:
    - The expected return from my dummy func is "Dummy."

    When:
    - I call the function to return the Dummy text.

    Then:
    - The result should be the same as the expected message.
    """
    expected_message = "Dummy"

    result = dummy_func()

    assert expected_message == result
