from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel, ValidationError
from datetime import datetime
from typing import List, Dict

from app.models.message import Message
from app.models.recipient import Recipient

# HTTP methods for recipients

from app.models.recipient_create import Recipient_create
from app.fake_db import fake_db

router = APIRouter()


#HTTP request method for creating a recipient
@router.post("/recipients/new/", response_model=Recipient)
def submit_recipient(recipient: Recipient_create, recipients: Dict[str, Recipient] = Depends(lambda: fake_db)):
    new_recipient_id = recipient.user_id
    if new_recipient_id not in recipients:
        try:
            new_recipient = Recipient(user_id=new_recipient_id)
            recipients[new_recipient_id] = new_recipient
            return new_recipient
        except ValidationError as e:
            raise HTTPException(status_code=400, detail=str(e))
    else:
        raise HTTPException(status_code=404, detail="Recipient allready exist")

#HTTP request method for listing all current recipients
@router.get("/recipients/", response_model=List[Recipient])
def list_recipients(recipients: Dict[str, Recipient] = Depends(lambda: fake_db)):
    return list(recipients.values())