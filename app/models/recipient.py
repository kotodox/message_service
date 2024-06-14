from app.models.message import Message
from pydantic import BaseModel
from typing import List
from datetime import datetime 


class Recipient(BaseModel):
    user_id: str
    messages: List[Message] = []
    message_counter: int = 1

    def add_message(self, message_content: str) -> Message:
        message = Message(
            id=self.message_counter,
            time_stamp=datetime.now(),
            message=message_content,
            fetched=False
        )
        self.messages.append(message)
        self.message_counter += 1
        return message