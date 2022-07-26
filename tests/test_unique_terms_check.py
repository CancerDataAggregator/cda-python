from cdapython import unique_terms
from tests.global_settings import host, table, localhost


def test_unique_terms_convert() -> None:
    d = unique_terms(
        "species", host=localhost, table="gdc-bq-sample.dev", show_sql=True
    )
    print(d.to_list())


test_unique_terms_convert()
