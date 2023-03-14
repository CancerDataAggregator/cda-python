from global_settings import integration_table, localhost

from cdapython import Q


def main():

    print(Q("sex = 'male'").to_json())
    print(Q('sex = "male"', lark=True).to_json())


main()
