from cdapython import Q
from tests.global_settings import host


def test_new_tables():
    myquery = Q('ethnicity = "hispanic or latino"').run(
        host=host, version="all_Subjects_v3_0_w_RS"
    )

    assert (str(myquery.sql).find("all_Subjects_v3_0_w_RS") != -1) == True
