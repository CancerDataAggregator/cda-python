from cdapython import Q
from tests.global_settings import integration_host


def test_url_change():
    Q.set_host_url(integration_host)
    assert Q.get_host_url().split(":")[2] == "8080/"
