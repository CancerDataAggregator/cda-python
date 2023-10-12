from cdapython import Q
from tests.global_settings import host


def test_tumor():
    tp = Q("SYMOBL = 'TP53%'").specimen.run(
        show_sql=True, host=host, include_total_count=False
    )
    assert len(tp.to_list()) > 0


test_tumor()
