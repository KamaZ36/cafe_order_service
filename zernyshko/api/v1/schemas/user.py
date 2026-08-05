from uuid import UUID

from pydantic import BaseModel, ConfigDict

from zernyshko.domain.entities.user import UserRole


class CreateUserSchema(BaseModel):
    phone_number: str


class CurrentUserResponseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    phone_number: str | None
    role: UserRole


class SendPhoneCodeSchema(BaseModel):
    phone_number: str


class PhoneLoginSchema(BaseModel):
    phone_number: str
    code: str


class LoginSchema(BaseModel):
    phone_number: str
    password: str


class ProvisionStaffSchema(BaseModel):
    phone_number: str
    password: str
    role: UserRole = UserRole.ADMIN


class AddItemToCartSchema(BaseModel):
    product_id: UUID
    quantity: int = 1
