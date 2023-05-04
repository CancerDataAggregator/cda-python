from cdapython import Q

slidequery = Q(
    'data_type = "Slide Image" OR source_material_type = "Slides" OR specimen_type = "slide"'
)
df = slidequery.subject.run(include="sex")

print(df.df_to_table())
