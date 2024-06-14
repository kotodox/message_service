from datetime import datetime 
from pydantic import BaseModel


#class for a message
class Message(BaseModel):
    id: int
    time_stamp: datetime
    message: str
    fetched: bool = False