from pydantic import BaseModel


class YooKassaWebhookObjectSchema(BaseModel):
    id: str


class YooKassaWebhookSchema(BaseModel):
    object: YooKassaWebhookObjectSchema
