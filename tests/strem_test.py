from typing import TYPE_CHECKING

from cdapython import Q
from tests.global_settings import host, project

if TYPE_CHECKING:
    from pandas import DataFrame


def test_primary_disease_type():
    q = Q('primary_disease_type = "Lung%"')
    print(q.to_json())

    q: DataFrame = q.run(host=host, table=project).to_dataframe()

    print(q.head())
    assert not q.empty
