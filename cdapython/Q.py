from typing import Tuple
from cdapython.Qbase import Qbase
from cdapython.Qparser import parser


class Q(Qbase):
    def __init__(self, *args: Tuple[str]) -> None:
        self.qbaseobj = self.parse(*args)
        
    def parse(self, args) -> Qbase:
        text = parser(str(args).strip())
        return text
        
    # def run(self,limit:int):
    #     return self.qbaseobj.run()


