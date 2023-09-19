from cdapython import Q
from tests.global_settings import host, integration_table

print(Q("SYMBOL = 'TP53'").specimen.run(show_sql=True, host=host))
