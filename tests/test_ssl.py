from cdapython import Q


def test_ssl():
    q1 = Q('ResearchSubject.id = "c5421e34-e5c7-4ba5-aed9-146a5575fd8d"')

    q1.run(verify=False)


test_ssl()
