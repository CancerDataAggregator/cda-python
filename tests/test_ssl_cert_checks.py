from cdapython import Q, columns
from tests.global_settings import host, table


def test_ssl_q() -> None:
    q = Q('id = "TCGA-13-1409"')
    r = q.run(verify=False, host=host, table=table)

    print(host, table)
    assert r.count == 1


print(host, table)
columns(verify=False, host=host, table=table, verbose=True)
