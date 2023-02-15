from cdapython import columns

print(
    columns(
        host="https://cancerdata.dsde-dev.broadinstitute.org/", description=False
    ).to_list(search_fields=["fieldName"], search_value="ma")
)

print(
    columns(
        host="https://cancerdata.dsde-dev.broadinstitute.org/", description=True
    ).to_list(
        search_fields=["fieldName", "endpoint"],
        search_value="tumor",
        allow_substring=True,
    )
)

print(
    columns(
        host="https://cancerdata.dsde-dev.broadinstitute.org/", description=True
    ).to_dataframe(
        search_fields=["description"], search_value="tumor", allow_substring=False
    )
)
