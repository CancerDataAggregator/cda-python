from global_settings import localhost

from cdapython import Q, unique_terms

u_sex = unique_terms("subject_id").run(host=localhost).get_all()

print(u_sex.to_dataframe())
# data = Q("sex").to_json()

# print(data)
# print(data._api_response["next_url"])
