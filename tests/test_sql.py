
from cdapython import Q


def test():
    qr = Q.sql("SELECT * FROM `gdc-bq-sample.integration.INFORMATION_SCHEMA.COLUMN_FIELD_PATHS` WHERE table_name = 'all_v1' Limit 5")
    assert qr[0]["table_schema"] == 'integration'
