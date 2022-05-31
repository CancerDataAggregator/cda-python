from rich import print

from cdapython.constant_variables import CDA_API_URL


def unverified_http() -> None:
    print(
        f"""[bold yellow]Unverified HTTPS request is being made to host'{CDA_API_URL}'. Adding certificate verification is strongly advised. See: https://urllib3.readthedocs.io/en/1.26.x/advanced-usage.html#ssl-warnings[/bold yellow]"""
    )


def deprecated_values(old: str, new: str) -> None:
    print(
        f" This Value {old} has been deprecated but will be converted it for you in the background please use the new value {new}"
    )
