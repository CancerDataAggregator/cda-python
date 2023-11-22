from pandas import json_normalize
from pandas.testing import assert_frame_equal
from cdapython import unique_terms, Q


def test_demonstrate_list_to_df_with_search_replacement():
    # new way
    df = json_normalize(
        data=unique_terms(col_name="primary_diagnosis_site", show_counts=True).to_list()
    )
    new_way = df.loc[
        df["primary_diagnosis_site"].str.contains("gland", case=False, na=False)
    ].reset_index(drop=True)
    # old way
    old_way = unique_terms("primary_diagnosis_site", show_counts=True).to_dataframe(
        search_fields="primary_diagnosis_site", search_value="gland"
    )

    assert_frame_equal(new_way, old_way)
