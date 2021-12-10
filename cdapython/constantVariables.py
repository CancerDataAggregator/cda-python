import os

VERSION = "2021.12.8"
DATABASETABLE_VERSION = "all_v2"
DATABASETABLE = "gdc-bq-sample.integration"
CDA_API_URL_ENV = "https://cda.cda-dev.broadinstitute.org"


val = os.environ.get("CDAPYTHON_ENV")

if val is not "development":
    __version__: str = VERSION
    CDA_API_URL: str = CDA_API_URL_ENV
    table_version: str = DATABASETABLE_VERSION
    default_table: str = DATABASETABLE
    project_name: str = default_table.split(".")[0]
else:
    print("DEBUG MODE")

    DATABASETABLE_VERSION = "all_v1"
    DATABASETABLE = "gdc-bq-sample.dev"
    CDA_API_URL_ENV = "http://34.71.0.127:8080"


    __version__: str = VERSION
    CDA_API_URL: str =  CDA_API_URL_ENV
    table_version: str = DATABASETABLE_VERSION
    default_table: str = DATABASETABLE
    project_name: str = default_table.split(".")[0]
