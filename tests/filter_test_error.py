from cdapython import Q, columns

# print(columns().to_list("specimen"))
# cptacsubjectquery = Q('subject_associated_project = "%cptac%"')
# df = cptacsubjectquery.subject.count.run(
#     include=("specimen_id specimen_type specimen_Files")
# ).to_dataframe()


# print(df)


columns().to_dataframe(include="Column_Name:specimen_Files")
