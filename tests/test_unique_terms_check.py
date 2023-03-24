from cdapython import unique_terms
from tests.global_settings import integration_host, integration_table


def test_unique_terms_convert() -> None:
    d = unique_terms(
        "species",
        host=integration_host,
        table=integration_table,
        show_sql=True,
        show_counts=True,
        async_req=True,
    ).to_dataframe()
    print(d)


test_unique_terms_convert()
