from cdapython import Q, columns, unique_terms
from tests.global_settings import integration_host, integration_table


def test_and_op():
    # print(columns(host=integration_host).to_dataframe())
    # print(
    #     unique_terms(
    #         host=integration_host, table=integration_table, col_name="ALLELE_NUM"
    #     ).to_list()
    # )
    q1 = Q("sex = '%'")
    q2 = Q("ALLELE_NUM = '%'").mutation

    q = q1.AND(q2).LIMIT(300).set_host(integration_host).set_table(integration_table)
    df = q.to_dataframe()
    assert len(df) > 3
    # a = q.to_dict()
    # for i in q:
    #     print(i)
