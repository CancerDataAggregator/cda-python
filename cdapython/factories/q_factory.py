from typing import TYPE_CHECKING, Any, Dict, Union

from . import BOOLEAN_QUERY, UNIQUE_TERMS

if TYPE_CHECKING:
    from cdapython.Q import Q


class AbstractFactory:
    @staticmethod
    def create(q_object: "Q") -> Union[Any, "Q"]:
        print("ran factories/q_factory.py AbstractFactory create")
        raise NotImplementedError


class QFactory:
    factories: Dict[str, AbstractFactory] = {}

    @staticmethod
    def add_factory(id: str, q_factory: Any) -> None:
        print("ran factories/q_factory.py QFactory add_factory")
        QFactory.factories[id] = q_factory

    @staticmethod
    def create_entity(id: str, q_object: "Q") -> "Q":
        print("ran factories/q_factory.py QFactory create_entity")
        if id != UNIQUE_TERMS:
            if q_object._get_system() != "":
                # TODO create custdom Exception for not support values
                raise Exception("System is not supported in this way for this query")

        return QFactory.factories[id].create(q_object)
