from cdapython import Q
from pandas import DataFrame, concat
from tests.global_settings import host

q = Q('identifier.value = "TCGA-E2-A10A"')
files_of_interest = q.file.run(host=host)


def iter_pages(result):
    df = result.to_dataframe()
    while result.has_next_page:
        result = result.next_page()
        df = concat([df, result.to_dataframe()])
    return df


dataTmp = DataFrame()
for i in files_of_interest.paginator(to_df=True):

    df_type = concat([dataTmp, i])

files_df = iter_pages(files_of_interest)
convert_dict = {
    "id": str,
    "researchsubject_specimen_id": str,
    "researchsubject_id": str,
    "subject_id": str,
}

files_df = files_df.astype(convert_dict)

print(files_df.info)


print(df_type.info)