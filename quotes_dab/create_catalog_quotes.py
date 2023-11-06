import sys

# path = "/Workspace/Users/d.martins@kigroup.de/.bundle/quotes_dab_bundle/dev/files"
from os import path
from pathlib import Path

path_2 = Path().cwd()
sys.path.append(path_2)

from quotes_dab.provide_config import sql_cmd_create_catalog, sql_cmd_create_schema

# Create Catalog
spark.sql(sql_cmd_create_catalog)


# Create Schema
spark.sql(sql_cmd_create_schema)
