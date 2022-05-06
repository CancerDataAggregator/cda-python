from cProfile import run
from cdapython import query
from tests.global_settings import localhost


def test():
    # q1 = q.run(verbose=True, host=localhost, format_type="tsv")
    # check = q.run(verbose=True, host=localhost, format_type="tsv") == q.run(verbose=True, host=localhost, format_type="tsv")
    # q1 = q.run(verify=False, host=host)
    # q1 = q.subjects.run(host=localhost)
    q2 = query('id = "TCGA-E2-A10A"')

    s = q2.subjects.run(host=localhost).sql
    d = q2.diagnosis.files.run(host=localhost).sql
    c = q2.list.run(host=localhost).sql
    print(s, end="\n\n")
    print(d, end="\n\n")
    print(c, end="\n\n")
    # for i in q1:
    #     print(i)
    # print(q1.to_dataframe().head())
    # print("id" in q1)


test()
