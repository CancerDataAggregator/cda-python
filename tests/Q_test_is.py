from cdapython import Q
from tests.global_settings import host, table


def test_is() -> None:
    d = Q("File.dbgap_accession_number IS NOT null")
    print(type(d.to_json()))


test_is()
