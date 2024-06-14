from pydantic import BaseModel
from datetime import datetime 


class Message_response(BaseModel):
    id: int
    time_stamp: datetime
    message: str
    fetched: bool