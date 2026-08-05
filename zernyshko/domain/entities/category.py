from uuid import UUID


class Category:
    def __init__(self, id: UUID, name: str) -> None:
        self._id = id
        self._name = name

    @property
    def id(self) -> UUID:
        return self._id

    @property
    def name(self) -> str:
        return self._name
