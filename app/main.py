from fastapi import FastAPI

from app.routes import messages, recipients


app = FastAPI()

app.include_router(messages.router)
app.include_router(recipients.router)

#fake_db: Dict[str, Recipient] = {}

@app.get("/")
def read_root():
    return {"message": "Welcome to the messaging service!"}

