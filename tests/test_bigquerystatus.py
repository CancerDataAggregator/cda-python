from cdapython import statusBigQuery


def test1():
    assert statusBigQuery() == 'everything is fine'

