from cdapython import Q
from tests.global_settings import host, localhost


def test_in_parser_testing() -> None:
    q1 = Q(
        "File.id IN ('256f12f9-f1f8-11e9-9a07-0a80fada099c','256f1b60-f1f8-11e9-9a07-0a80fada099c','256f2c22-f1f8-11e9-9a07-0a80fada099c','256f14ca-f1f8-11e9-9a07-0a80fada099c')"
    ).file.run(host=host)

    q2 = (
        Q(
            'age_at_death IS null OR age_at_death = 0 AND sex = "male" OR sex = "female" '
        )
        .run(host=host)
        .to_dataframe()
    )


test_in_parser_testing()
