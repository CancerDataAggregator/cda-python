from cdapython import unique_terms
from tests.global_settings import host, table, localhost


def test_unique_terms_convert() -> None:
    d = unique_terms(
        "species",
        host="http://35.192.60.10:8080/",
        table="gdc-bq-sample.dev",
        show_sql=True,
        show_counts=True,
    ).to_dataframe()


test_unique_terms_convert()
