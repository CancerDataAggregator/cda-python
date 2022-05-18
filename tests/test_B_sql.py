from time import sleep

from cdapython import Q


def test_q_sql():
    qr = Q.sql(
        "SELECT * FROM `gdc-bq-sample.cda_mvp.INFORMATION_SCHEMA.COLUMN_FIELD_PATHS` WHERE table_name = 'v3' Limit 5",
        verify=False,
    )
    assert qr[0]["table_schema"] == "cda_mvp"
