from typing import TYPE_CHECKING, Any, Dict, Union

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
        return QFactory.factories[id].create(q_object)
