from global_settings import localhost

from cdapython import Q

a = Q("sex = 'male'").mutation.run(host=localhost)
print(a)
print(a.to_dataframe())
print(a.next_page())
