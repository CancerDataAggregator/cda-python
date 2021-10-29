from typing import Optional


VERSION = "2021.10.29"
DATABASETABLE_VERSION = "all_v2"
DATABASETABLE = "gdc-bq-sample.integration"
CDA_API_URL_ENV = "https://cda.cda-dev.broadinstitute.org"

__version__: Optional[str] = VERSION
CDA_API_URL: Optional[str] = CDA_API_URL_ENV
table_version: Optional[str] = DATABASETABLE_VERSION
default_table: Optional[str] = DATABASETABLE

project_name: Optional[str] = (
    default_table.split(".")[0] if isinstance(default_table, str) else None
)
