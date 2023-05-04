from cdapython import Q


def test_like_equals_conversion():
    v = Q('primary_disease_type = "Lung%"')
    check_dict = v.to_dict()
    assert check_dict["node_type"] == "LIKE"
    assert check_dict["r"]["value"] == "Lung%"
