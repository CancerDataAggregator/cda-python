from cdapython import Q

integration_host = "http://35.192.60.10:8080/"
integration_table = "gdc-bq-sample.dev"
print(
    Q("sex = 'male'").run(
        table=integration_table, host=integration_host, show_sql=True, limit=100
    )
)
