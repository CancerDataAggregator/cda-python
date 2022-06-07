from cdapython import Q
from tests.global_settings import host
from matplotlib import pyplot as plot


def test_is() -> None:
    d = Q("File.dbgap_accession_number is not null").file.run(
        host=host, async_call=True
    )
    # print(d.to_dataframe()["subject_id"][0])
    assert d.to_dataframe()["subject_id"][0] == ("TARGET-51-PAJPFB")


test_is()
