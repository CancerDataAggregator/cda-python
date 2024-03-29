from cdapython import Q, columns, unique_terms
from tests.global_settings import host, project


def test_and_op():
    # print(
    #     columns(host=host, table=project).to_filter(search_fields=["fieldName"], search_value="ALLELE").to_dataframe()
    # )
    # print(
    #     unique_terms(
    #         host=integration_host, table=integration_table, col_name="ALLELE_NUM"
    #     ).to_list()
    # )
    q1 = Q("sex = '%'")
    q2 = Q("Allele = '%'").mutation

    q = q1.AND(q2).LIMIT(300).set_host(host).set_project(project)
    df = q.run().to_dataframe()

    assert len(df) > 3
    # a = q.to_dict()
    # for i in q:
    #     print(i)


test_and_op()
