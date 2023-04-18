from cdapython import columns

print(
    columns(
        host="https://cancerdata.dsde-dev.broadinstitute.org/", description=False
    ).to_list(filters="ma")
)

print(
    columns(
        host="https://cancerdata.dsde-dev.broadinstitute.org/", description=True
    ).to_list(filters="ma")
)
