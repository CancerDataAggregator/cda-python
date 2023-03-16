from global_settings import integration_table, localhost

from cdapython import Q


def main():

    # print(Q("sex = 'male'").to_json())
    all_data = Q(
        "sex = REPLACE(REPLACE(sex,'fe',''), 'male', '' )", lark=True
    ).to_json()
    print(all_data)


main()
