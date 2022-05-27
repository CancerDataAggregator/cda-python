from cdapython import query
from cdapython.utility import columns

from tests.global_settings import host


def test() -> None:
    q2 = query("sex = 'male'")
    print(type(q2), q2)
    # print(q2.to_json())
    q3 = q2.researchsubject.run(host=host).to_dataframe()
    print(d3)
    # se = q3.run(host=localhost).to_dataframe()
    # d = q3.file.run(host=localhost).to_dataframe()
    # c = q2.run(host=localhost).to_dataframe()
    # f = q2.specimen.file.run(host=localhost).to_dataframe()
    # w = q2.count.run(host=localhost).to_dataframe()
    # r = q2.research_subject.file.run(host=localhost).to_dataframe()
    # print(s)
    # print(se)
    # print(columns().to_list())
    # print(r, end="\n\n")
    # print(f, end="\n\n")
    # print(s, end="\n\n")
    # print(d, end="\n\n")
    # print(c, end="\n\n")
    # print(w, end="\n\n")


test()
