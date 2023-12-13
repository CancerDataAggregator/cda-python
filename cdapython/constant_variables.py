"""
This module is made for Q Global Constants/

"""


class Constants:
    """
    This class Holds Q Global Constants used in Http methods
    """

    _VERSION: str = "2023.9.12"
    _DATABASETABLE_VERSION: str = "all_merged_subjects_v3_4_final"
    _DATABASETABLE: str = "broad-dsde-prod.cda_prod"
    _CDA_API_URL_ENV: str = "https://cancerdata.ah-cda6.bee.envs-terra.bio"
    _DATABASETABLE_FOR_FILES: str = "broad-dsde-prod.cda_prod"
    _DATABASETABLE_VERSION_FOR_FILES: str = "all_merged_files_v3_4_final"

    __version__: str = _VERSION
    cda_api_url: str = _CDA_API_URL_ENV
    table_version: str = _DATABASETABLE_VERSION
    default_table: str = _DATABASETABLE
    project_name: str = default_table.split(".", maxsplit=1)[0]
    default_file_table: str = _DATABASETABLE_FOR_FILES

    @staticmethod
    def version() -> str:
        print("ran constant_variables version")
        """
        This is used to get version
        Returns:
            str: _description_
        """
        return Constants()._VERSION
