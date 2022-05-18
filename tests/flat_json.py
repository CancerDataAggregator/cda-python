from cdapython import query
from cdapython.utility import columns
from tests.global_settings import localhost


def test():
    q2 = query('id = "TCGA-E2-A10A"')
    q3 = q2.subject

    s = q3.run(host=localhost).to_list()
    se = q3.run(host=localhost).to_dataframe()
    # d = q3.file.run(host=localhost).to_dataframe()
    # c = q2.run(host=localhost).to_dataframe()
    # f = q2.specimen.file.run(host=localhost).to_dataframe()
    # w = q2.count.run(host=localhost).to_dataframe()
    # r = q2.research_subject.file.run(host=localhost).to_dataframe()
    print(s)
    print(se)
    print(columns().to_list())
    # print(r, end="\n\n")
    # print(f, end="\n\n")
    # print(s, end="\n\n")
    # print(d, end="\n\n")
    # print(c, end="\n\n")
    # print(w, end="\n\n")


test()
