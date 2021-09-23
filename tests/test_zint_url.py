from cdapython import Q


def test_url_change():
    Q.set_host_url("http://34.71.0.127:8080")
    assert Q.get_host_url().split(":")[2] == "8080"
