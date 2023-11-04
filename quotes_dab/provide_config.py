"""
This variable stores the name of the Databricks profile to be used for authentication.
Ensure that this profile is configured in the .databrickscfg file.
"""
profile_to_authenticate = "KIPROFILE"

"""
List available categories to extract quotes

"""
category_list = [
    "age",
    "alone",
    "amazing",
    "anger",
    "architecture",
    "art",
    "attitude",
    "beauty",
    "best",
    "birthday",
]


"""
Define the use case for the script.

This variable specifies the use case for the script, which can be either "dbx" or "dab." The choice of use case influences how the script will behave or which configurations will be applied.

Attributes:
    use_case (str): The use case, which can be either "dbx" (for one use case) or "dab" (for another use case).
"""
use_case = "dab"


"""
Path to include thorugh module `sys`

"""

"""
Define Catalog Name and command to create it.

This variable defines the name of the catalog to be created and the SQL command to create it.

Attributes:
    catalog_name (str): The name of the catalog.
    sql_cmd_create_catalog (str): The SQL command to create the catalog.
"""
catalog_name = "catalog_quotes"
sql_cmd_create_catalog = f"CREATE CATALOG IF NOT EXISTS {catalog_name}"

"""
Define Schema Name and command to create it.

This variable defines the name of the schema to be created and the SQL command to create it.

Attributes:
    schema_name (str): The name of the schema.
    sql_cmd_create_schema (str): The SQL command to create the schema.
"""
schema_name = f"quotes_{use_case}"
sql_cmd_create_schema = f"CREATE SCHEMA IF NOT EXISTS {catalog_name}.{schema_name}"

"""
Define Paths Location.

This section defines the file paths for different purposes.

Attributes:
    path_landing_quotes_dbx (str): The landing path for quotes in the dbx use case.
    path_schema_autoloader (str): The path for schema autoloading.
"""
path_landing_quotes_dbx = f"/mnt/landing/quotes_{use_case}"
path_schema_autoloader = f"/mnt/{use_case}"
