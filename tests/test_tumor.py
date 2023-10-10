from cdapython import Q
from tests.global_settings import host, integration_table, localhost


def test_tumor():
    tp = Q("SYMBOL = 'TP53'").specimen.run(
        show_sql=True, host=localhost, include_total_count=False
    )
    assert len(tp.to_list()) > 0


test_tumor()
