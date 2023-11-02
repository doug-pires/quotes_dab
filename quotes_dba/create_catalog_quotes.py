from quotes_dba.provide_config import sql_cmd_create_catalog, sql_cmd_create_schema

# Create Catalog
spark.sql(sql_cmd_create_catalog)


# Create Schema
spark.sql(sql_cmd_create_schema)
