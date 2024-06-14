import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.fake_db import fake_db

client = TestClient(app)

@pytest.fixture(autouse=True)
def setup_and_teardown():
    # Setup before each test
    fake_db.clear()  # Clear the recipients dictionary before each test
    yield
    # Teardown after each test
    fake_db.clear()  # Clear the recipients dictionary after each test

def test_create_recipient():
    response1 = client.post("/recipients/new", json={"something_else": "user1"})
    response2 = client.post("/recipients/new", json={"user_id": "user1"})
    response3 = client.post("/recipients/new", json={"user_id": "user1"})
    response4 = client.post("/recipients/new", json={"user_id": "user1", "something_else": "123"})
    assert response1.status_code == 422
    assert response2.status_code == 200
    assert response3.status_code == 404
    assert response4.status_code == 404
    assert response2.json() == {
        "user_id": "user1",
        "messages": [],
        "message_counter": 1
    }

def test_list_recipients():
    response1 = client.get("/recipients/")
    for i in range(20):
        client.post("/recipients/new", json={"user_id": f"user{i}"})
    response2 = client.get("/recipients/")
    assert response1.status_code == 404
    assert len(response2.json()) ==20 


def test_create_message():
    client.post("/recipients/new", json={"user_id": "user1"})
    response1 = client.post("/messages/send/", json={"recipient_id": "user2", "message": "Hello, user1!"})
    response2 = client.post("/messages/send/", json={"recipient_id": "user1", "message": "Hello, user1!"})
    response3 = client.post("/messages/send/", json={"Something_else": "user1", "message": "Hello, user1!"})
    response4 = client.post("/messages/send/", json={"recipient_id": "user1", "message": "Hello, user1!, something_else: 123"})
    assert response1.status_code == 404
    assert response2.status_code == 200
    assert response3.status_code == 422
    assert response4.status_code == 200
    message2 = response2.json()
    assert message2["message"] == "Hello, user1!"
    assert message2["fetched"] == False

def test_fetch_new_messages():
    client.post("/recipients/new", json={"user_id": "user1"})
    client.post("/messages/send/", json={"recipient_id": "user1", "message": "Hello, user1!"})
    response1 = client.get("/messages/fetch/new/user2")
    response2 = client.get("/messages/fetch/new/user1")
    #response1 = client.get("/messages/fetch/new/", json={"recipient_id": "user2"})
    #response2 = client.get("/messages/fetch/new/", json={"recipient_id": "user1"})
    client.post("/messages/send/", json={"recipient_id": "user1", "message": "Hello, user1! msg 2"})
    response3 = client.get("/messages/fetch/new/user1")
    assert response1.status_code == 404
    assert response2.status_code == 200
    messages = response2.json()
    messages2 = response3.json()
    assert len(messages) == 1
    assert len(messages2) == 1
    assert messages[0]["message"] == "Hello, user1!"
    assert messages[0]["fetched"] == True

def test_fetch_messages_with_pagination():
    client.post("/recipients/new/", json={"user_id": "user1"})
    for i in range(20):
        client.post("/messages/send/", json={"recipient_id": "user1", "message": f"Message {i}"})
    response = client.get("/messages/fetch/user1?start=0&stop=10")
    response2 = client.get("/messages/fetch/user1?start=0&stop=30")
    response3 = client.get("/messages/fetch/user1?start=20&stop=10")
    response4 = client.get("/messages/fetch/user2?start=20&stop=10")
    assert response.status_code == 200
    assert response2.status_code == 200
    messages = response.json()
    assert len(messages) == 10
    assert len(response2.json()) == 20
    assert len(response3.json()) == 1
    assert len(response4.json()) == 1
    assert messages[0]["message"] == "Message 0"
    assert messages[-1]["message"] == "Message 9"

def test_amount_messages():
    client.post("/recipients/new/", json={"user_id": "user1"})
    for i in range(10):
        client.post("/messages/send/", json={"recipient_id": "user1", "message": f"Message {i}"})
    response = client.get("/messages/amount/user1").json()
    response2 = client.get("/messages/amount/user2")
    assert response == 10
    assert response2.status_code == 404

def test_delete_message():
    client.post("/recipients/new/", json={"user_id": "user1"})
    response = client.post("/messages/send/", json={"recipient_id": "user1", "message": "Hello, user1!"})
    message = response.json()
    response = client.delete(f"/messages/delete/user1/{message['id']}")
    response2 = client.delete("/messages/delete/user1/10")
    amount = client.get("/messages/amount/user1").json()
    assert response.status_code == 200
    assert response2.status_code == 404
    assert response.json() == message
    assert amount == 0

def test_delete_multiple_messages():
    client.post("/recipients/new/", json={"user_id": "user1"})
    for i in range(10):
        client.post("/messages/send/", json={"recipient_id": "user1", "message": f"Message {i}"})
    response = client.post("/messages/delete/multiple/user1", json=[1, 2, 3, 100])
    amount = client.get("/messages/amount/user1").json()
    assert response.status_code == 200
    response_json = response.json()
    error_msg = response_json["errors"]
    deleted_msg = response_json["deleted_messages"]
    assert len(deleted_msg) == 3
    assert deleted_msg[0]["id"] == 1
    assert deleted_msg[1]["id"] == 2
    assert deleted_msg[2]["id"] == 3
    assert len(error_msg) == 1
    assert error_msg[0]["message_id"] == 100
    assert amount == 7
    