from cdapython import Q
from time import sleep


def test_bigquery_status():
    sleep(1)
    assert Q.statusbigquery() == "everything is fine"
