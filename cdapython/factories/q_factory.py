from typing import TYPE_CHECKING, Any, Dict, Union

from . import BOOLEAN_QUERY, UNIQUE_TERMS

if TYPE_CHECKING:
    from cdapython.Q import Q


class AbstractFactory:
    @staticmethod
    def create(q_object: "Q") -> Union[Any, "Q"]:
        raise NotImplementedError


class QFactory:
    factories: Dict[str, AbstractFactory] = {}

    @staticmethod
    def add_factory(id: str, q_factory: Any) -> None:
        QFactory.factories[id] = q_factory

    @staticmethod
    def create_entity(id: str, q_object: "Q") -> "Q":
        if id != UNIQUE_TERMS:
            if q_object._get_system() != "":
                # TODO create custdom Exception for not support values
                raise Exception("System is not supported in this way for this query")

        return QFactory.factories[id].create(q_object)
