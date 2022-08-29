class Constants:
    _VERSION: str = "2022.8.29"
    _DATABASETABLE_VERSION: str = "all_Subjects_v3_0_final"
    _CLIENT_VERSION: str = "3.0.0"
    _DATABASETABLE: str = "broad-dsde-prod.cda_prod"
    _CDA_API_URL_ENV: str = "https://cda.datacommons.cancer.gov/"
    _DATABASETABLE_FOR_FILES: str = "broad-dsde-prod.cda_prod"
    _DATABASETABLE_VERSION_FOR_FILES: str = "all_Files_v3_0_final"

    __version__: str = _VERSION
    CDA_API_URL: str = _CDA_API_URL_ENV
    table_version: str = _DATABASETABLE_VERSION
    default_table: str = _DATABASETABLE
    project_name: str = default_table.split(".")[0]
    default_file_table: str = _DATABASETABLE_FOR_FILES
