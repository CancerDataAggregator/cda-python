from cdapython import unique_terms
from tests.global_settings import host, table


def test_unique_terms_convert() -> None:
    d = unique_terms(
        "species",
        host=host,
        table=table,
        show_sql=True,
        show_counts=True,
    ).to_dataframe()


test_unique_terms_convert()
