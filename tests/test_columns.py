from cdapython import Q, columns

# from tests.global_settings import host, table, localhost


def test_columns():
    integration_host = "http://35.192.60.10:8080/"
    Q.set_default_project_dataset("gdc-bq-sample.dev")
    cols = columns(host=integration_host).to_list()
    assert isinstance(cols, list) is True


test_columns()
