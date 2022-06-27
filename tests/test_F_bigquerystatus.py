from time import sleep

from cdapython import Q


def test_bigquery_status():
    sleep(1)
    assert Q.bigquery_status() == "everything is fine"


print(Q.bigquery_status())
