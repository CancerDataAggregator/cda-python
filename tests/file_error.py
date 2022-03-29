from cdapython import Q

q1 = Q("identifier.system = 'GDC'")
q6 = Q("File.identifier.system = 'GDC'")
q16 = q6


print(q16.run(host="http://localhost:8080" ,format="csv"))
