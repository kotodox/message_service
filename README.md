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
            "name": "John Doe",
            "email": "john.doe@example.com"
        }
        ```

2. **Submit a Message**

    - **URL**: `/messages/`
    - **Method**: `POST`
    - **Request Body**:
        ```json
        {
            "recipient_id": "user1",
            "message": "Hello, user1!"
        }
        ```

3. **Fetch New Messages**

    - **URL**: `/messages/fetch/new/{recipient_id}`
    - **Method**: `GET`

4. **Delete a Single Message**

    - **URL**: `/messages/{recipient_id}/{message_id}`
    - **Method**: `DELETE`

5. **Delete Multiple Messages**

    - **URL**: `/messages/{recipient_id}`
    - **Method**: `DELETE`
    - **Request Body**:
        ```json
        [1, 2, 3]
        ```

6. **Fetch Messages with Pagination**

    - **URL**: `/messages/{recipient_id}?start=0&stop=10`
    - **Method**: `GET`

### Running Tests

To run tests, ensure you have `pytest` installed. You can install it using Pipenv:

```bash
pipenv install pytest
```