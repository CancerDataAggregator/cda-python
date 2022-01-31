from cdapython import Q
q = Q('id = "TCGA-13-1409"') # note the double quotes for the string value
#q1 = Q('id = "tcga-13-1409"')
r = q.run(version = "all_v2_1", verbose=False)
# df = r.filter("Files",to_DF=True).to_csv("test.csv")

print(r)