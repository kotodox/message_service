# FastAPI Message Service

## Overview

This is a simple message service built with FastAPI. The service allows you to:
1. Submit a message to a defined recipient.
2. Fetch new messages.
3. Delete a single message.
4. Delete multiple messages.
5. Fetch messages ordered by time.

## Features

- **Recipient Management**: Create recipients identified by user ID.
- **Message Management**: Send messages to recipients, fetch new messages, and delete messages.
- **Message Ordering**: Fetch messages ordered by time.

## Installation

### Prerequisites

- Python 3.7+
- pip
- pipenv (for managing virtual environments)

### Steps

1. **Clone the repository**

    ```bash
    git clone <repository-url>
    cd <repository-directory>
    ```

2. **Install Pipenv**

    If you don't have Pipenv installed, you can install it using pip:

    ```bash
    pip install pipenv
    ```

3. **Install dependencies**

    Navigate to the project directory and install the dependencies using Pipenv:

    ```bash
    pipenv install
    ```

## Running the Application

1. **Activate the virtual environment**

    ```bash
    pipenv shell
    ```

2. **Run the FastAPI server**

    ```bash
    uvicorn app.main:app --reload
    ```

    This will start the server on `http://127.0.0.1:8000`.

## Usage

### Endpoints

1. **Create a Recipient**

    - **URL**: `/recipients/new/`
    - **Method**: `POST`
    - **Request Body**:
        ```json
        {
            "user_id": "user1",
        }
        ```
    - **Example**:
        ```bash
        curl -X POST "http://127.0.0.1:8000/recipients/new/" -H "Content-Type: application/json" -d '{"user_id": "user1"}'
        ```

2. **List of all Recipients**

    - **URL**: `/recipients/`
    - **Method**: `GET`
    - **Example**:
    ```bash
    curl -X GET "http://127.0.0.1:8000/recipients/"
    ```


3. **Submit a Message**

    - **URL**: `/messages/send/`
    - **Method**: `POST`
    - **Request Body**:
        ```json
        {
            "recipient_id": "user1",
            "message": "Hello, user1!"
        }
        ```
        - **Example**:
        ```bash
        curl -X POST "http://127.0.0.1:8000/messages/send/" -H "Content-Type: application/json" -d '{"recipient_id": "user1", "message": "Hello, user1!"}'
        ```

4. **Fetch New Messages**

    - **URL**: `/messages/fetch/new/{recipient_id}`
    - **Method**: `GET`
    - **Example**:
        ```bash
        curl -X GET "http://127.0.0.1:8000/messages/fetch/new/user1"
        ```

5. **Fetch Messages within certain index of all messages sorted according to timestamp**

    - **URL**: `/messages/fetch/{recipient_id}?start=0&stop=10`
    - **Method**: `GET`
    - **Example**:
        ```bash
        curl -X GET "http://127.0.0.1:8000/messages/fetch/user1?start=0&stop=10"
        ```

6. **Fetch amount of messages recipient has**

    - **URL**: `/messages/amount/{recipient_id}`
    - **Method**: `GET`
    - **Example**:
        ```bash
        curl -X GET "http://127.0.0.1:8000/messages/amount/user1"
        ```

7. **Delete a Single Message**

    - **URL**: `/messages/delete/{recipient_id}/{message_id}`
    - **Method**: `DELETE`
    - **Example**:
        ```bash
        curl -X DELETE "http://127.0.0.1:8000/messages/delete/user1/1"
        ```

8. **Delete Multiple Messages**

    - **URL**: `/messages/delete/multiple/{recipient_id}`
    - **Method**: `POST`
    - **Request Body**:
        ```json
        [1, 2, 3]
        ```
    - **Example**:
        ```bash
        curl -X POST "http://127.0.0.1:8000/messages/delete/multiple/user1" -H "Content-Type: application/json" -d '[1, 2, 3]'
        ```


### Running Tests

To run tests, ensure you have `pytest` installed. You can install it using Pipenv:

```bash
pipenv install pytest
```