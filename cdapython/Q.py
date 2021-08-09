from cdapython.constantVariables import CDA_API_URL, table_version
from typing import Tuple
from cdapython.Qbase import Qbase
from cdapython.Qparser import parser


class Q(Qbase):
    def __init__(self, *args: Tuple[str]) -> None:
        self.qbaseobj = self.parse(*args)
        
    def parse(self, args) -> Qbase:
        text = parser(str(args).strip())
        return text

    def run(self, offset: int = 0, limit: int = 1000, version: str = table_version, host: str = CDA_API_URL, dry_run: bool = False):
        return self.qbaseobj.run(offset, limit, version, host, dry_run)


