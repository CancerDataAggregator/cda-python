from cdapython import Q


def test_bigquery_status():
    assert Q.statusbigquery() == "everything is fine"
