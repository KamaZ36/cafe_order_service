from enum import Enum
from uuid import UUID, uuid7


class UserRole(str, Enum):
    CUSTOMER = "CUSTOMER"
    ADMIN = "ADMIN"
    MANAGER = "MANAGER"


class User:
    def __init__(
        self,
        id: UUID,
        phone_number: str | None,
        role: UserRole = UserRole.CUSTOMER,
        password_hash: str | None = None,
    ) -> None:
        self._id = id
        self._phone_number = phone_number
        self._role = role
        self._password_hash = password_hash

    @classmethod
    def create(cls, phone_number: str | None = None) -> "User":
        return cls(id=uuid7(), phone_number=phone_number)

    @property
    def id(self) -> UUID:
        return self._id

    @property
    def phone_number(self) -> str | None:
        return self._phone_number

    @property
    def role(self) -> UserRole:
        return self._role

    @property
    def password_hash(self) -> str | None:
        return self._password_hash

    def set_phone_number(self, phone_number: str) -> None:
        self._phone_number = phone_number

    def promote_to_staff(self, role: UserRole, password_hash: str) -> None:
        self._role = role
        self._password_hash = password_hash

    def is_staff(self) -> bool:
        # Меню и заказы — общая зона ответственности всего персонала кафе
        return self._role in (UserRole.ADMIN, UserRole.MANAGER)

    def is_admin(self) -> bool:
        # ADMIN — технический аккаунт с доступом к управлению пользователями,
        # это единственное, чего нет у MANAGER
        return self._role == UserRole.ADMIN
