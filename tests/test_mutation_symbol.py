from cdapython import Q
from tests.global_settings import host, localhost, project


# in postgres Symobol dose not Exist it is changed to Hugo_Symbol
def test_mutation_symbol():
    symbol = Q("Hugo_Symbol LIKE 'TP53%'").run(host=host, show_sql=True)
    print(symbol)

    assert len(symbol.to_list()) != 0
