# Databricks notebook source

# COMMAND ----------
path = spark.conf.get("bundle.sourcePath")
import sys

sys.path.append(path)


import dlt
import pyspark.sql.functions as F
from pyspark.sql import Column, DataFrame

from quotes_dab.common import add_hash_col, add_metadata_cols, group_by_counting_rows
from quotes_dab.provide_config import path_landing_quotes_dbx, path_schema_autoloader

# COMMAND ----------

# MAGIC %md
# MAGIC ## Define Properties to help build FAIR data assets

# COMMAND ----------

properties_bronze = {
    "layer": "bronze",
    "ownership": "Douglas Pires",
    "department": "Data team",
    "Is_PII": "False",
    "freshness": "Daily",
}
properties_silver = {
    "layer": "silver",
    "ownership": "Douglas Pires",
    "department": "Data team",
    "Is_PII": "False",
    "freshness": "Daily",
}
properties_gold = {
    "layer": "gold",
    "ownership": "Douglas Pires",
    "department": "Data team",
    "Is_PII": "False",
    "freshness": "Daily",
}

# COMMAND ----------

# MAGIC %md
# MAGIC # Bronze table
# MAGIC ## Ingestion using AutoLoader and add metadata columns

# COMMAND ----------

options_quotes_df = {
    "format": "cloudFiles",
    "cloudFiles.format": "json",
    "cloudFiles.schemaLocation": path_schema_autoloader,
    "cloudFiles.schemaEvolutionMode": "addNewColumns",
    "InferSchema": "true",
    # When Auto Loader infers the schema, a rescued data column is automatically added to your schema as _rescued_data. You can rename the column or include it in cases where you provide a schema by setting the option rescuedDataColumn.
    "cloudFiles.inferColumnTypes": "true",
    "multiline": "true",
}

# COMMAND ----------


@dlt.table(
    comment="Ingestion Quote data to Delta Table Bronze, adding metadata columns",
    table_properties=properties_bronze,
)
def bronze_table_quotes():
    df = (
        spark.readStream.format("cloudFiles")
        .options(**options_quotes_df)
        .load(path_landing_quotes_dbx)
    )
    df_quotes = df.transform(add_metadata_cols)
    return df_quotes


# COMMAND ----------

# MAGIC %md
# MAGIC # Silver Tables

# COMMAND ----------

cols_to_hash = ["quote", "author", "category"]


@dlt.table(
    comment="Silver table, generating SK to uniquely identify unique quotes concatenating author, quote and category",
    table_properties=properties_silver,
)
def silver_quotes():
    df = dlt.read_stream("bronze_table_quotes")
    df_quotes_add_hash_key = df.transform(
        add_hash_col, cols_to_hash=cols_to_hash, new_col_name="hash_quote"
    ).select("quote", "author", "category", "hash_quote")
    return df_quotes_add_hash_key


# COMMAND ----------

# MAGIC %md
# MAGIC # Gold Tables

# COMMAND ----------


@dlt.table(
    comment="Gold Table, aggragated quotes by category",
    table_properties=properties_gold,
)
def gold_aggregated():
    df = dlt.read("silver_quotes")
    df_grouped_by_category = df.transform(group_by_counting_rows, col="category")
    return df_grouped_by_category


# COMMAND ----------

col_to_duplicate_and_drop = "hash_quote"


@dlt.table(
    comment="Gold Table, removing duplicates on hash_key that uniquely identify the quote",
    table_properties=properties_gold,
)
def gold_quotes_for_report():
    df = dlt.read("silver_quotes")
    df_gold = df.dropDuplicates([col_to_duplicate_and_drop]).drop(
        col_to_duplicate_and_drop
    )
    return df_gold
