from cdapython import Q
from tests.global_settings import host


def test_limit_node_exist():
    limit_node = Q("sex = 'm'").LIMIT(1000)
    assert limit_node._get_limit() == 1000


def test_offset_node_exist():
    limit_node = Q("sex = 'm'").OFFSET(1000)
    assert limit_node._get_offset() == 1000


def test_server_limit():
    values = Q("sex = 'm'").LIMIT(1).run(host=host)
    assert len(values.to_list()) == 1


def test_server_limit_2():
    values = Q("sex = 'm'").LIMIT(2).run(host=host)
    assert len(values.to_list()) != 1


def test_server_offest_and_limit():
    values = Q("sex = 'm'").LIMIT(1).OFFSET(0).run(host=host)
    values_2 = Q("sex = 'm'").LIMIT(1).OFFSET(1).run(host=host)

    assert values.to_list() != values_2.to_list()
    assert values.to_list() == values.to_list()
