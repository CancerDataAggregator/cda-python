from cdapython.Q import Q


class Entity(Q):
    @property
    def file(self) -> "Q":
        raise NotImplementedError

    @property
    def count(self) -> "Q":
        raise NotImplementedError
