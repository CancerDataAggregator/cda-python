from cdapython import Q

print(
    Q.from_file(
        field_to_search="ethnicity",
        file_to_search="tests/bquxjob_23ec205_184e89499c1.csv",
        key="ethnicity",
    ).subject.run()
)


# print(
#     Q.from_file(
#         field_to_search="subject_id",
#         file_to_search="tests/testids.txt",
#     )
#     .subject.run(show_sql=True, verify=False)
#     .to_dataframe()
# )
