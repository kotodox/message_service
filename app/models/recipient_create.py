from pydantic import BaseModel


#Class for variables needed to create new recipient
class Recipient_create(BaseModel):
    user_id: str

