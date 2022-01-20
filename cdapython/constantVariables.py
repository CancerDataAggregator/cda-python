
VERSION = "2022.1.20"
DATABASETABLE_VERSION = "all_v2"
DATABASETABLE = "gdc-bq-sample.integration"
CDA_API_URL_ENV = "https://cda.cda-dev.broadinstitute.org"


__version__: str = VERSION
CDA_API_URL: str = CDA_API_URL_ENV
table_version: str = DATABASETABLE_VERSION
default_table: str = DATABASETABLE
project_name: str = default_table.split(".")[0]
