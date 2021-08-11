
from typing import Tuple
from cdapython.Q import Q
from cdapython.Qparser import parser
from cdapython.constantVariables import table_version, CDA_API_URL
from abc import ABCMeta, abstractmethod


class IQ(metaclass=ABCMeta):
    "The Builder Interface"

    @staticmethod
    @abstractmethod
    def build_part_left():
        "Build part a"

    @staticmethod
    @abstractmethod
    def build_part_right():
        "Build part b"

    @staticmethod
    @abstractmethod
    def build_part_op():
        "Build part c"

    @staticmethod
    @abstractmethod
    def get_result():
        "Return the final product"


class QBuilder(IQ):
    def build_part_left():
        return parser()
    
    



