import sys

bundle_src_path = sys.argv[1]
sys.path.append(bundle_src_path)
from quotes_dab.provide_config import sql_cmd_create_catalog, sql_cmd_create_schema

# Create Catalog
spark.sql(sql_cmd_create_catalog)


# Create Schema
spark.sql(sql_cmd_create_schema)
