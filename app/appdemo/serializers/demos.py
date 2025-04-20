from ninja import Schema
from pydantic import BaseModel


class SvActFormFileDemoPostIn(Schema):
    name: str


class DemoQueueSchema(BaseModel):
    """
    Schema for the demo queue.
    """

    message: str
