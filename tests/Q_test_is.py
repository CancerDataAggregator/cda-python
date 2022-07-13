from cdapython import Q
from tests.global_settings import host, table
from matplotlib import pyplot as plot


def test_is() -> None:
    d = Q("File.dbgap_accession_number IS NOT null").file.run(
        host=host, async_call=True, table=table, verify=True
    )
    # print(d.to_dataframe()["subject_id"][0])
    assert d.to_dataframe()["subject_id"][0] == ("TARGET-51-PAJPFB")


test_is()
