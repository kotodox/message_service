from pydantic import BaseModel


#Class for variables needed to create new message
class Message_create(BaseModel):
    recipient_id: str
    message: str
