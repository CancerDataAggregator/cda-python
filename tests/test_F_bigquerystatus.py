from cdapython import Q
from time import sleep


def test_bigquery_status():
    sleep(1)
    assert Q.bigquery_status() == "everything is fine"
