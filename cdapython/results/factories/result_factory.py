from __future__ import annotations

from typing import TYPE_CHECKING, Any, Dict

if TYPE_CHECKING:
    from cdapython.results.result import Result


class AbstractFactory:
    @staticmethod
    def create(q_object: Result) -> Result:
        print("ran result_factory.py AbstractFactory create")
        raise NotImplementedError


class ResultFactory:
    """
    The ResultFactory class is made to create objects
    Returns:
        _type_: _description_
    """

    factories: Dict[str, AbstractFactory] = {}

    @staticmethod
    def add_factory(id: str, result_factory: Any) -> None:
        print("ran result_factory.py add_factory")
        ResultFactory.factories[id] = result_factory

    @staticmethod
    def create_entity(id: str, result_object: Any) -> Result:
        print("ran result_factory.py create_entity")
        return ResultFactory.factories[id].create(result_object)
