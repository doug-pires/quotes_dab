import pyspark.sql.functions as F
from pyspark.sql import DataFrame

from quotes_dab.config_logging import get_stream_logger

logger = get_stream_logger(__name__)


def add_metadata_cols(df: DataFrame) -> DataFrame:
    """
    Add metadata columns to a Spark DataFrame.
    Usually used in Databricks Autoloader
    https://docs.databricks.com/en/ingestion/file-metadata-column.html

    This function takes a Spark DataFrame and adds two columns, 'ingestion_datetime'
    and 'file_name', by extracting information from the '_metadata' column if it exists.

    Parameters:
    df (DataFrame): The input Spark DataFrame that may contain the '_metadata' column.

    Returns:
    DataFrame: A new Spark DataFrame with 'ingestion_datetime' and 'file_name' columns
    added if '_metadata' exists in the input DataFrame, or the original DataFrame if
    '_metadata' is not present.
    """
    df = df.withColumn(
        "file_modification_time", F.col("_metadata.file_modification_time")
    ).withColumn("file_name", F.col("_metadata.file_name"))

    return df


def drop_columns(df: DataFrame, cols_to_drop: list[str]) -> DataFrame:
    """
    Drops specified columns from a DataFrame.

    Args:
        df (DataFrame): The input DataFrame.
        cols_to_drop (list[str]): List of column names to be dropped.

    Returns:
        DataFrame: A new DataFrame with specified columns removed.
    """
    df = df.drop(*cols_to_drop)
    return df


def cast_cols(df: DataFrame, cols_to_cast: dict[str, str]) -> DataFrame:
    """
    Casts specified columns to the provided data types in a DataFrame.

    Args:
        df (DataFrame): The input DataFrame.

        cols_to_cast (dict[str, str]): A dictionary where keys are column names
            and values are the target data types for casting.

    Returns:
        DataFrame: A new DataFrame with specified columns cast to the target data types.

    Example:
        You can use this function to cast specific columns in a DataFrame.
        ```python
        from pyspark.sql import SparkSession
        spark = SparkSession.builder.appName("example").getOrCreate()
        data = [("John", "30", "true"), ("Alice", "25", "false")]
        columns = ["name", "age", "is_student"]
        df = spark.createDataFrame(data, columns)
        df.show()
        +-----+---+----------+
        | name|age|is_student|
        +-----+---+----------+
        | John| 30| true|
        |Alice| 25| false|
        +-----+---+----------+

        cast_types = {"age": "int", "is_student": "boolean"}
        new_df = cast_cols(df, cast_types)
        new_df.show()
        +-----+---+----------+
        | name|age|is_student|
        +-----+---+----------+
        | John| 30| true|
        |Alice| 25| false|
        +-----+---+----------+
        ```

    """
    cols = list(cols_to_cast.keys())

    for col in cols:
        type = cols_to_cast.get(col)
        df = df.withColumn(col, F.col(col).cast(type))
    return df


def add_hash_col(
    df: DataFrame, cols_to_hash: list[str], new_col_name: str = "hash_col"
) -> DataFrame:
    """
    Add a new column to the DataFrame that contains the hash value of the concatenated values of specified columns.

    Args:
        df (DataFrame): The input DataFrame to which the new column will be added.
        cols_to_hash (list[str]): A list of column names to be concatenated and hashed.
        new_col_name (str, optional): The name of the new column to store the hash values. Defaults to "hash_col".

    Returns:
        DataFrame: A new DataFrame with an additional column containing the hash values.
    """
    expr = [F.col(col_name) for col_name in cols_to_hash]

    df = df.withColumn(new_col_name, F.md5(F.concat(*expr)))
    return df


def group_by_counting_rows(df: DataFrame, col: str):
    """
    Group a DataFrame by a specified column and count the occurrences of each group.

    Parameters:
    df (DataFrame): The input DataFrame to be grouped.
    col (str): The name of the column by which to group the DataFrame.

    Returns:
    DataFrame: A new DataFrame with the groups and their corresponding counts.
    """
    df_grouped = df.groupBy(col).count()
    return df_grouped
