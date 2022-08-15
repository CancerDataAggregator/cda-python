from cdapython import unique_terms, columns

print(
    unique_terms("File.imaging_modality", show_sql=True).to_list(
        filters="", exact=False
    )
)
