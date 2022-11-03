from cdapython import Q


def test_bigquery_status():
    assert Q.bigquery_status() == "everything is fine"


test_bigquery_status()
