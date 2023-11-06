import sys

# path = "/Workspace/Users/d.martins@kigroup.de/.bundle/quotes_dab_bundle/dev/files"
# from os import path
from pathlib import Path

path_file = Path(__file__).parent.as_posix()
path_file_parent = Path(__file__).parent.parent.as_posix()


print("Path Obsolute Parent:", path_file)
print("Path Obsolute Parents:", path_file_parent)


sys.path.append(path_file_parent)

from quotes_dab.provide_config import sql_cmd_create_catalog, sql_cmd_create_schema

# Create Catalog
spark.sql(sql_cmd_create_catalog)


# Create Schema
spark.sql(sql_cmd_create_schema)
