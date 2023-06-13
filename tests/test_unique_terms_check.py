from cdapython import unique_terms
from tests.global_settings import host


def test_unique_terms_convert() -> None:
    d = unique_terms(
        col_name="species",
        host=host,
        show_sql=True,
        show_counts=True,
    ).to_dataframe()


test_unique_terms_convert()
