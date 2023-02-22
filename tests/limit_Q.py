from global_settings import localhost

from cdapython import Q

integration_host = localhost
integration_table = "gdc-bq-sample.dev"


a = Q("sex = 'male' LIMIT 10,000")


a = a.run(host=integration_host, table=integration_table)


print(a)
print(a.get_all())
# for i in a.paginator():
#     print(i)

# print(a.to_dataframe())
