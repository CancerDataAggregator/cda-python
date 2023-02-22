from global_settings import localhost

from cdapython import unique_terms

print(unique_terms("sex", show_counts=True, host=localhost).df_to_table())
