from typing import Any, Dict


class QFactory:
    factories: Dict[str, Any] = {}

    @staticmethod
    def add_factory(id, q_factory):
        QFactory.factories[id] = q_factory

    @staticmethod
    def create_entity(id, q_object):
        return QFactory.factories[id].create(q_object)
