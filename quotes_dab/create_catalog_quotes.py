import sys

# path = "/Workspace/Users/d.martins@kigroup.de/.bundle/quotes_dab_bundle/dev/files"
from os import path

sys.path.append(path)

from quotes_dab.provide_config import sql_cmd_create_catalog, sql_cmd_create_schema

# Create Catalog
spark.sql(sql_cmd_create_catalog)


# Create Schema
spark.sql(sql_cmd_create_schema)
