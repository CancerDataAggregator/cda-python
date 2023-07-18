from global_settings import integration_table, localhost

from cdapython import Q

print(
    Q("SYMBOL = 'TP53'").specimen.run(
        show_sql=True, host=localhost, table=integration_table
    )
)
