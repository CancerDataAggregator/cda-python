from cdapython.Q import Q


class Entity(Q):
    @property
    def file(self) -> "Q":
        print("ran factories/entity.py file")
        raise NotImplementedError

    @property
    def count(self) -> "Q":
        print("ran factories/entity.py count")
        raise NotImplementedError
