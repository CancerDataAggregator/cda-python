from cdapython import Q
from cdapython.results.result import Result
from tests.global_settings import host, table
from tests.fake_result import FakeResultData
from unittest import mock


result = [
    {
        "id": "GENIE-DFCI-007281",
        "identifier": [{"system": "GDC", "value": "GENIE-DFCI-007281"}],
        "species": "homo sapiens",
        "sex": "male",
        "race": "white",
        "ethnicity": "not hispanic or latino",
        "days_to_birth": -16071,
        "subject_associated_project": ["GENIE-DFCI"],
        "vital_status": "Not Reported",
        "days_to_death": None,
        "cause_of_death": None,
    }
]


def checking_test():
    q1 = Q(
        "ResearchSubject.id IN ['C0EF0C13-3109-47CF-9BA4-076AB7EB7660',' 6AA44F89-FCE7-46FE-A1CB-874CD5EFA4A4']"
    ).AND(Q('sex = "male"'))
    print(q1)
    assert q1.query.to_dict()["l"]["node_type"] == "IN"
    r = q1.run(host=host, table=table)
    print(r)
