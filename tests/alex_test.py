from cdapython import Q, columns
from tests.global_settings import localhost, table


def test_alex():
    r = (
        Q("stage = 'Stage I'")
        .OR("stage = 'Stage II'")
        .AND('primary_diagnosis_site = "Breast Invasive Carcinoma"')
    )

    check_dict = r.to_dict()
    assert check_dict["node_type"] == "AND"
    assert check_dict["l"]["node_type"] == "OR"
    assert check_dict["l"]["l"]["l"]["node_type"] == "column"
    assert check_dict["l"]["l"]["r"]["node_type"] == "quoted"
    assert check_dict["l"]["r"]["r"]["node_type"] == "quoted"
