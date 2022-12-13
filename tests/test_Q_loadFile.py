from cdapython import Q

print(
    Q.from_file(
        field_to_search="subject_id",
        file_to_search="tests/allrepeatedcases.csv",
        key="1",
    ).subject.run(show_sql=True)
)
