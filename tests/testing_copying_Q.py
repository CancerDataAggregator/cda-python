from cdapython import Q
from tests.global_settings import localhost, host

q1 = Q('ResearchSubject.primary_disease_type = "Lung%"')

q1.subject.run(host=host)
q1.files.run(host=host)
