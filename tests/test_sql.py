from cdapython import Q


def test():
    qr = Q.sql(
        "SELECT * FROM `gdc-bq-sample.cda_mvp.INFORMATION_SCHEMA.COLUMN_FIELD_PATHS` WHERE table_name = 'v3' Limit 5"
    )
    assert qr[0]["table_schema"] == "cda_mvp"
