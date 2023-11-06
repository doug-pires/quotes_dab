import sys

# path = "/Workspace/Users/d.martins@kigroup.de/.bundle/quotes_dab_bundle/dev/files"
# from os import path
from pathlib import Path

path_absolute = Path().cwd().absolute()
path_abs_parent = Path().cwd().absolute().parent
path_abs_parents = Path().cwd().absolute().parents

print("Path Obsolute:", path_absolute)
print("Path Obsolute Parent:", path_abs_parent)
print("Path Obsolute Parents:", path_abs_parents)


sys.path.append(path_absolute.as_posix())

from quotes_dab.provide_config import sql_cmd_create_catalog, sql_cmd_create_schema

# Create Catalog
spark.sql(sql_cmd_create_catalog)


# Create Schema
spark.sql(sql_cmd_create_schema)
