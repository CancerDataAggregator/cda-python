# Versioning Year Month Day of last push
VERSION: str = "2022.3.21"
DATABASETABLE_VERSION: str = "all_v3_0_subjects_meta"
DATABASETABLE: str = "gdc-bq-sample.dev"
CDA_API_URL_ENV: str = "https://cda.cda-dev.broadinstitute.org"
DATABASETABLE_FOR_FILES: str = "gdc-bq-sample.dev"
DATABASETABLE_VERSION_FOR_FILES: str = "all_v3_0_Files"

__version__: str = VERSION
CDA_API_URL: str = CDA_API_URL_ENV
table_version: str = DATABASETABLE_VERSION
default_table: str = DATABASETABLE
project_name: str = default_table.split(".")[0]
default_file_table: str = DATABASETABLE_FOR_FILES
file_table_version: str = DATABASETABLE_VERSION_FOR_FILES
