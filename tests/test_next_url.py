from cdapython import Q

data = Q("sex = 'male'").run()
print(data)
