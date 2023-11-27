from cdapython import Q
from tests.global_settings import host

q1 = Q('researchsubject_identifier_system = "PDC"')
q2 = Q('researchsubject_identifier_system = "GDC"')
q3 = Q('identifier_system = "IDC"')

q = q3.FROM(q1.FROM(q2))
print("first")
with open("first.json", "w") as f:
    f.write(q.to_json())
a = Q(
    "identifier_system = 'IDC' FROM researchSubject_identifier_system = 'PDC'  FROM researchSubject_identifier_system = 'GDC' ",
).to_json()


b = Q(
    "identifier_system = 'IDC' FROM researchSubject_identifier_system = 'PDC'  FROM researchSubject_identifier_system = 'GDC'",
    debug=True,
).to_json()
print("lark")
with open("lark.json", "w") as f:
    f.write(b)
print("-" * 110)
print("Q parse")
with open("parse.json", "w") as f:
    f.write(a)
