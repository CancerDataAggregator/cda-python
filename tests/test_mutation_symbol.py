from cdapython import Q
from tests.global_settings import host, localhost, project


# in postgres Symbol dose not Exist it is changed to Hugo_Symbol
def test_mutation_symbol():
    symbol = Q("SYMBOL LIKE 'TP53%'").run(host=host, show_sql=True)
    print(symbol)
    assert len(symbol.to_list()) != 0
