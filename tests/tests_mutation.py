from cdapython import Q

Q.set_default_project_dataset("gdc-bq-sample.dev")

print(
    Q('primary_diagnosis_site = "Kidney"').mutation.count.run(
        host="http://localhost:8080"
    )
)
