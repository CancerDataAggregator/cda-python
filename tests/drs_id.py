from tests.global_settings import host


from cdapython import Q
from cdapython.utils.utility import get_host_url


def main():
    # print(Q("sex = 'male'").to_json())
    all_data = (
        Q("sex = REPLACE(REPLACE(sex,'fe',''), 'male', '' ) AND id = 1", debug=True)
        .SELECT("id,sex")
        .set_host(host)
        .run()
    )
    print(all_data)
    # intergation = all_data.set_host(integration_host)
    # prod = all_data.set_host(production_host)
    # all_data.set_host(localhost).set_project(integration_table).to_dataframe()


main()
