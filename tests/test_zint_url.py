from cdapython import Q, get_host_url, set_host_url
from tests.global_settings import integration_host


def test_url_change():
    set_host_url(integration_host)
    assert get_host_url().split(":")[2] == "8080/"
