from cdapython import Q
from tests.global_settings import host, project


def test_mutation_symbol():
    symbol = Q("SYMBOL LIKE 'TP53%'").researchsubject.run(
        host=host, table=project, show_sql=True
    )

    assert len(symbol.to_list()) != 0
