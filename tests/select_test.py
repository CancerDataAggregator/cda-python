from cdapython import Q

a = (
    Q("sex = 'male' AND NOT vital_status = 'Dead'  ")
    .set_host("http://localhost:8080")
    .set_project("gdc-bq-sample.yet_another_sandbox")
    .SELECT("vital_status,sex")
)
print(a.to_json())
print(a.run(show_sql=True))
