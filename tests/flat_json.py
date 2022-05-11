from cdapython import query
from tests.global_settings import localhost


def test():
    q2 = query('id = "TCGA-E2-A10A"')
    q3 = q2.subject

    s = q3.run(host=localhost).to_dataframe()
    d = q3.files.run(host=localhost).to_dataframe()
    c = q2.run(host=localhost).to_dataframe()
    f = q2.specimen.files.run(host=localhost).to_dataframe()
    w = q2.run(host=localhost).to_dataframe()
    r = q2.research_subject.files.run(host=localhost).to_dataframe()
    print(r, end="\n\n")
    print(f, end="\n\n")
    print(s, end="\n\n")
    print(d, end="\n\n")
    print(c, end="\n\n")
    print(w, end="\n\n")
    for i in r:
        print(i)
    print(r.to_dataframe().head())
    print("id" in r)


test()
