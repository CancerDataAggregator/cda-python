from cdapython import Q


def id_test():
    q = Q('id = "TCGA-E2-A10A"')  # note the double quotes for the string value
    check_dict = q.to_dict()
    # assert check_dict["node_type"] == "="
    print(check_dict)


id_test()
