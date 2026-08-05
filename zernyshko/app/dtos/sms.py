from dataclasses import dataclass


@dataclass(frozen=True, eq=False)
class SendSmsDTO:
    phone_number: str
    code: str
