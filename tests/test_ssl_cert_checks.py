from cdapython import Q

def test_ssl_sql():
    qr = Q.sql(
        "SELECT * FROM `gdc-bq-sample.cda_mvp.INFORMATION_SCHEMA.COLUMN_FIELD_PATHS` WHERE table_name = 'v3' Limit 5",
        verify=False,
    )
    assert qr[0]["table_schema"] == "cda_mvp"


def test_ssl_Q():
    q = Q('id = "TCGA-13-1409"') 
    r = q.run(verify=False)
    assert r.count == 1


test_ssl_Q()