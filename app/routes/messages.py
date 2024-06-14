
from fastapi import HTTPException, APIRouter, Depends, Query
from pydantic import ValidationError
from typing import List, Dict

from app.models.message import Message
from app.models.recipient import Recipient

from app.models.message_create import Message_create
from app.fake_db import fake_db

router = APIRouter()

#HTTP request method for sending message to recipient
@router.post("/messages/send/", response_model=Message)
def submit_message(msg: Message_create, recipients: Dict[str, Recipient] = Depends(lambda: fake_db)):
    recipient_id = msg.recipient_id
    message_content = msg.message
    if recipient_id not in recipients:
        raise HTTPException(status_code=404, detail="Recipient not found")
    try:
        message = recipients[recipient_id].add_message(message_content)
        return message
    except ValidationError as e:
        raise HTTPException(status_code=400, detail=str(e))


#HTTP request method for fetching all new messages of a recipient
@router.get("/messages/fetch/new/{recipient_id}", response_model=List[Message])
#@router.get("/messages/fetch/new/", response_model=List[Message])
def fetch_new_messages(recipient_id: str, recipients: Dict[str, Recipient] = Depends(lambda: fake_db)):
    if recipient_id not in recipients:
        raise HTTPException(status_code=404, detail="Recipient not found")
    new_messages = [msg for msg in recipients[recipient_id].messages if not msg.fetched]
    for msg in new_messages:
        msg.fetched = True
    return new_messages

#HTTP request method for fetching certain amount of messages sorted according to timestamp
@router.get("/messages/fetch/{recipient_id}", response_model=List[Message])
def fetch_messages(recipient_id: str, stop: int = Query(None, ge=1, description="The number of messages to return"), start: int = Query(0, ge=0, description="The number of messages to return"), recipients: Dict[str, Recipient] = Depends(lambda: fake_db)):
    if recipient_id not in recipients:
        raise HTTPException(status_code=404, detail="Recipient not found")
    recipient = recipients[recipient_id]
    sorted_messages = sorted(recipient.messages, key=lambda msg: msg.time_stamp)
    total_amount_msg = len(sorted_messages)
    if(stop > total_amount_msg or stop == None):
        stop = total_amount_msg
    if(start > stop):
        start = stop-1
    return sorted_messages[start:stop]


#HTTP request method for fetching amount of messages a recipient has recieved
@router.get("/messages/amount/{recipient_id}", response_model=int)
def amount_msg(recipient_id: str, recipients: Dict[str, Recipient] = Depends(lambda: fake_db)):
    if recipient_id not in recipients:
        raise HTTPException(status_code=404, detail="Recipient not found")
    total_amount_msg = len(recipients[recipient_id].messages)
    return total_amount_msg

#HTTP request method for deleting a specific message a recipient has recieved
@router.delete("/messages/delete/{recipient_id}/{message_id}", response_model=Message)
def delete_message(recipient_id: str, message_id: int, recipients: Dict[str, Recipient] = Depends(lambda: fake_db)):
    if recipient_id not in recipients:
        raise HTTPException(status_code=404, detail="Recipient not found")
    recipient = recipients[recipient_id]
    for msg in recipient.messages:
        if msg.id == message_id:
            recipient.messages.remove(msg)
            return msg
    raise HTTPException(status_code=404, detail="Message not found")


#HTTP request method for deleting multiple messages a recipient has recieved
@router.post("/messages/delete/multiple/{recipient_id}", response_model=Dict[str, List])
def delete_multiple_messages(recipient_id: str, ids: List[int], recipients: Dict[str, Recipient] = Depends(lambda: fake_db)):
    if recipient_id not in recipients:
        raise HTTPException(status_code=404, detail="Recipient not found")
    recipient = recipients[recipient_id]
    deleted_messages = []
    errors = []
    for message_id in ids:
        for msg in recipient.messages:
            if msg.id == message_id:
                recipient.messages.remove(msg)
                deleted_messages.append(msg)
                break
        else:
            errors.append({"message_id": message_id, "error": "Message not found"})
    if not deleted_messages:
        raise HTTPException(status_code=404, detail="No messages found")
    return {"deleted_messages": deleted_messages, "errors": errors}





