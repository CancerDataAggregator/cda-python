from cdapython import unique_terms

projlist = []
for i in unique_terms("file_associated_project").paginator(to_list=True):
    projlist.extend(i)
print(len(projlist))
