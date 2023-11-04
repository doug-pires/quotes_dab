### Adding a Hash Column to a DataFrame

In this example, we will demonstrate how to use the `add_hash_col` function to add a hash column to a DataFrame. We'll be using Apache Spark for DataFrame operations.

### Function Description

The `add_hash_col` function is designed to add a new column to a DataFrame that stores the hash value of concatenated values from specified columns. It takes the following arguments:

- `df` (DataFrame): The input DataFrame to which the new column will be added.
- `cols_to_hash` (list of strings): A list of column names to be concatenated and hashed.
- `new_col_name` (string, optional): The name of the new column to store the hash values. It defaults to "hash_col."

Here's the function code:

```python
def add_hash_col(
    df: DataFrame, cols_to_hash: list[str], new_col_name: str = "hash_col"
) -> DataFrame:
    expr = [F.col(col_name) for col_name in cols_to_hash]

    df = df.withColumn(new_col_name, F.md5(F.concat(*expr)))
    return df


from pyspark.sql import SparkSession
from my_module import add_hash_col

# Create a Spark session
spark = SparkSession.builder.appName("DataFrameHashing").getOrCreate()


# Sample DataFrame
data = [("John", "Doe", 30),
        ("Jane", "Smith", 25),
        ("Bob", "Johnson", 40)]
columns = ["first_name", "last_name", "age"]
df = spark.createDataFrame(data, columns)

# Columns to hash
cols_to_hash = ["first_name", "last_name"]

# Show the updated DataFrame
hashed_df.show()
```

## Results
| first_name | last_name | age | hash_col             |
| ---------- | --------- | --- | -------------------- |
| John       | Doe       | 30  | 6a02a05d57b8e18a6... |
| Jane       | Smith     | 25  | 5875b470e6b0f35a2... |
| Bob        | Johnson   | 40  | caf76821891f74b2...  |




