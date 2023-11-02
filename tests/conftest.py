import os

import pytest
from pyspark.sql import SparkSession
from pyspark.sql.types import (
    BooleanType,
    IntegerType,
    MapType,
    StringType,
    StructField,
    StructType,
)


@pytest.fixture(scope="session")
def spark_session() -> SparkSession:
    """
    PyTest fixture for creating a SparkSession.

    This fixture creates a SparkSession and automatically closes it at the end of the test session.

    Returns:
        SparkSession: An instance of SparkSession ready for use in tests.

    Example:
        ```python
        def test_spark_operations(spark_session):
            # Perform Spark operations using the provided SparkSession.
            df = spark_session.read.csv("test_data.csv")
            assert df.count() > 0
        ```
    """
    # Create a SparkSession
    spark = (
        SparkSession.builder.appName("pytest_spark_fixture")
        .master("local[1]")
        .getOrCreate()
    )

    # Set any necessary configuration options
    spark.conf.set("spark.sql.shuffle.partitions", "2")

    # Yield the SparkSession to the tests
    yield spark

    # Teardown - stop the SparkSession
    spark.stop()


@pytest.fixture(scope="session")
def dummy_data() -> list:
    """
    PyTest fixture for providing dummy data as a list.

    Returns:
        list: A list containing the data schema and data rows.

    Example:
        ```python
        def test_data_processing(dummy_data):
            schema, data = dummy_data
            # Perform data processing using the provided schema and data.
            assert len(data) > 0
        ```
    """
    fields = [
        StructField("name", StringType(), nullable=True),
        StructField("age", IntegerType(), nullable=True),
        StructField("job", StringType(), nullable=True),
        StructField("country", StringType(), nullable=True),
        StructField("is_married", BooleanType(), nullable=True),
    ]
    schema = StructType(fields)

    data = [
        ("Douglas", 31, "Engineer", "Brazil", True),
        ("Tifa", 25, "Doctor", "Germany", False),
        ("Marc", 88, "Retired", "Germany", True),
        ("Alberto", 35, "Mechanic", "Italy", True),
    ]

    return [schema, data]


@pytest.fixture(scope="session")
def dummy_metadata_data() -> list:
    """
    PyTest fixture for providing dummy data with metadata as a list.

    Returns:
        list: A list containing the data schema and data rows with metadata.

    Example:
        ```python
        def test_metadata_processing(dummy_metadata_data):
            schema, data = dummy_metadata_data
            # Perform metadata processing using the provided schema and data with metadata.
            assert len(data) > 0
        ```
    """
    data = [
        {
            "country": "USA",
            "_metadata": {
                "file_path": "path/to/data",
                "file_name": "test.json",
                "file_modification_time": "2021-07-02 01:05:21",
            },
        },
        {
            "country": "Portugal",
            "_metadata": {
                "file_path": "path/to/other",
                "file_name": "example.json",
                "file_modification_time": "2021-12-20 02:06:21",
            },
        },
    ]

    # Define the schema for the DataFrame
    schema = StructType(
        [
            StructField("country", StringType(), nullable=True),
            StructField(
                "_metadata", MapType(StringType(), StringType()), nullable=True
            ),
        ]
    )

    return [schema, data]


@pytest.fixture(scope="function")
def mock_authentication_databricks(mocker):
    """
    Mock the authentication function for Databricks.

    This function provides a mock object for the authentication function used in Databricks integration.
    REMEMBER:When it comes to mocking, we ALWAYS mock where the function is USED. Even though the `authenticate_databricks()` is from other module
    Args:
        mocker: The mocker object provided by PyTest for mocking.

    Returns:
        Mock: A mocked authentication function.

    Example:
        ```python
        def test_databricks_integration(mock_authentication_databricks):
            # Test Databricks integration with authentication mock.
            mock_authentication_databricks.return_value = "Authentication Successful"
            result = databricks_integration()
            assert result == "Authentication Successful"
        ```
    """
    path_to_mock = "quotes.request_quote.authenticate_databricks"

    w_mock = mocker.patch(path_to_mock)
    return w_mock


@pytest.fixture(scope="function")
def api_key_mock_local(mocker):
    # api_key = os.getenv("API_KEY_NINJAS")
    path_to_mock = "quotes.request_quote.get_api_key"
    mock_api_key = mocker.patch(path_to_mock, api_key="44sa5adaKey")
    return mock_api_key


@pytest.fixture(scope="session")
def api_key_integration():
    api_key = os.getenv("API_KEY_NINJAS")
    return api_key
