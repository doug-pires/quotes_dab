import hashlib

import pytest
from chispa import assert_df_equality
from pyspark.sql.types import LongType, StringType, StructField, StructType
from pytest import fixture

from quotes_dba.common import (
    add_hash_col,
    add_metadata_cols,
    cast_cols,
    drop_columns,
    group_by_counting_rows,
)


def test_if_function_dropped_the_list_columns(
    spark_session: fixture, dummy_data: fixture
):
    """
     Given the Data and Schema from Dummy Data, we create the Dataframe 'Persons' and specify a list of columns to drop.

     When we call the 'drop_columns' function on a DataFrame, the specified columns should be removed.

     Then the resulting DataFrame should only contain the expected columns.

    Args:
        spark_session: A PySpark session used for DataFrame creation.
        dummy_data: A fixture providing data and schema.
    """
    schema = dummy_data[0]
    data = dummy_data[1]
    df_persons = spark_session.createDataFrame(data=data, schema=schema)

    cols_to_be_removed = ["job", "city"]

    df_dropped_cols = df_persons.transform(
        drop_columns, cols_to_drop=cols_to_be_removed
    )

    assert cols_to_be_removed not in df_dropped_cols.columns


def test_if_columns_provided_was_casted(spark_session: fixture, dummy_data: fixture):
    """
     Given the Data and Schema from Dummy Data, we create two DataFrames:
     1. 'df_persons_correct_schema' with the CORRECT SCHEMA.
     2. 'df_wrong_schema' with the WRONG SCHEMA containing all STRINGTYPE columns.

     When we call the 'cast_cols' function to cast the specified columns on the 'df_wrong_schema',

     Then it should return a DataFrame with the expected schema, as in 'df_persons_correct_schema',
     using Chispa for schema comparison.

    Args:
        spark_session: A PySpark session used for DataFrame creation.
        dummy_data: A fixture providing data and schema.
    """
    schema = dummy_data[0]
    data = dummy_data[1]

    df_persons_correct_schema = spark_session.createDataFrame(data=data, schema=schema)

    fields_wrong = [
        StructField("name", StringType(), nullable=True),
        StructField("age", StringType(), nullable=True),
        StructField("job", StringType(), nullable=True),
        StructField("country", StringType(), nullable=True),
        StructField("is_married", StringType(), nullable=True),
    ]

    schema_wrong = StructType(fields_wrong)
    df_wrong_schema = spark_session.createDataFrame(data=data, schema=schema_wrong)

    cols_to_be_casted = {"age": "int", "is_married": "boolean"}

    df_fixed = df_wrong_schema.transform(cast_cols, cols_to_cast=cols_to_be_casted)

    assert_df_equality(df_persons_correct_schema, df_fixed)


@pytest.mark.parametrize(
    "expected_metadata_columns", ["file_name", "file_modification_time"]
)
def test_function_to_extract_metadata_from_dataframe(
    spark_session: fixture,
    dummy_metadata_data: fixture,
    expected_metadata_columns: fixture,
):
    """
    Given the Data and Schema from Dummy Data containing Metadata,
    we create the Dataframe 'Countries' containing Metadata.

    When we call the 'add_metadata_cols' function to add columns for extracting metadata,

    Then we should assert that the expected metadata columns were added to the DataFrame.

    Args:
        spark_session: A PySpark session used for DataFrame creation.
        dummy_metadata_data: A fixture providing data and schema with a column as MapType()
        expected_metadata_columns: A fixture containing the metadata columns I want to extract
    """
    schema = dummy_metadata_data[0]
    data = dummy_metadata_data[1]
    df_countries = spark_session.createDataFrame(data=data, schema=schema)

    df_with_metadata = df_countries.transform(add_metadata_cols)

    assert expected_metadata_columns in df_with_metadata.columns


def test_if_hash_col_was_created(dummy_data: fixture, spark_session: fixture):
    """
    Test the 'add_hash_col' function to check if a 'hash_col' was created and contains the expected values.

    Steps:
    1. Given the Data and Schema from Dummy Data, we create the Dataframe 'df_persons'.
    2. When the first row containing values 'Douglas | 31 | Engineer | Brazil | True' is hashed using md5.
    3. We call the function to create a 'hash_col' and hash the specified columns.
    4. Then we should have a column named 'hash_col' in the resulting DataFrame.
    5. We check the first hash value for the values of the first row against the expected hash value.

    Args:
        dummy_data: Fixture providing data and schema.
        spark_session: PySpark session for DataFrame creation.
    """
    schema = dummy_data[0]
    data = dummy_data[1]
    df_persons = spark_session.createDataFrame(data=data, schema=schema)

    row_1 = "Douglas31EngineerBraziltrue"
    expected_hash = hashlib.md5(row_1.encode()).hexdigest()

    cols_to_be_hashed = df_persons.columns
    df_w_col_hashed = df_persons.transform(add_hash_col, cols_to_hash=cols_to_be_hashed)

    assert "hash_col" in df_w_col_hashed.columns
    assert expected_hash == df_w_col_hashed.collect()[0]["hash_col"]


def test_group_by_function_to_agg_by_specific_column(
    dummy_data: fixture, spark_session: fixture
):
    """
    Test the 'group_by_counting_rows' function to aggregate rows by 'country' and compare the result to the expected aggregated DataFrame.

    Steps:
    1. Given the 'df_persons' DataFrame.
    2. We expect to have an aggregated DataFrame by 'country' with specific schema.
    3. When we call the function to group by 'country'.
    4. The result should be a DataFrame with the same structure as 'df_expected_agg_by_country'.
    5. We perform a DataFrame equality check, ignoring nullable and row order.

    Args:
        dummy_data: Fixture providing data and schema.
        spark_session: PySpark session for DataFrame creation.
    """
    schema = dummy_data[0]
    data = dummy_data[1]
    df_persons = spark_session.createDataFrame(data=data, schema=schema)

    expected_agg_fields = [
        StructField("country", StringType(), nullable=True),
        StructField("count", LongType(), nullable=True),
    ]
    schema_df_agg_by_country = StructType(expected_agg_fields)

    data_country_agg = [("Germany", 2), ("Italy", 1), ("Brazil", 1)]

    df_expected_agg_by_country = spark_session.createDataFrame(
        data=data_country_agg, schema=schema_df_agg_by_country
    )

    df_grouped_by_country = group_by_counting_rows(df=df_persons, col="country")

    assert_df_equality(
        df_expected_agg_by_country,
        df_grouped_by_country,
        ignore_nullable=True,
        ignore_row_order=True,
    )
