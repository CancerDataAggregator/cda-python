from cdapython import Q, columns

# print(columns().to_list("specimen"))
# cptacsubjectquery = Q('subject_associated_project = "%cptac%"')
# df = cptacsubjectquery.subject.count.run(
#     include=("specimen_id specimen_type specimen_Files")
# ).to_dataframe()


# print(df)


columns().to_dataframe()


Q("GDC_FILTER = 'NonExonic;bitgt'").mutation.ORDER_BY("sex:-1").run(
    host="https://cancerdata.dsde-dev.broadinstitute.org/",
    table="broad-dsde-dev.cda_dev",
).to_dataframe(include="sample_barcode_tumor:TCG,sample_barcode_tumor:TCG")
