import sys

from global_settings import integration_table, localhost

from cdapython import Q, columns, get_drs_id, unique_terms


def main():

    print(Q("sex = 'male'").SELECT("MAX (1) REPLACE(i, 'a','')").to_json())


main()
