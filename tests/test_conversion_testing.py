from cdapython import Q
from tests.global_settings import integration_host, integration_table


def test_conversion() -> None:
    q1 = Q("age_at_diagnosis > 50*365")
    q2 = Q('subject_associated_project = "TCGA-OV"')
    q = q1.AND(q2)

    r = q.run(host=integration_host, table=integration_table)
    print(r.to_dataframe().head())
