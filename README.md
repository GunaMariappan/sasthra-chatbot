# Sasthra Product AI Chatbot

A domain-restricted AI chatbot that answers only questions about Sasthra products.
Users sign up, log in, and chat. Answers come only from product information stored
in MongoDB.

## Tech stack

- Frontend: React (Vite)
- Backend: Python, FastAPI
- Database: MongoDB (PyMongo)
- AI: Google Gemini REST API
- Auth: bcrypt password hashing, JWT

## How it works

React -> FastAPI -> JWT check -> domain check -> MongoDB product data
-> safe prompt -> Gemini REST API -> answer check -> React

Questions that are not about Sasthra products are rejected before Gemini is called.
If the information is not in the database, the chatbot says it is not available.

## Setup

Requirements: Python 3.12+, Node.js 20+, MongoDB running locally.

Backend:

    cd backend
    python -m venv venv
    .\venv\Scripts\Activate.ps1
    pip install -r requirements.txt

Create `backend/.env` from `backend/.env.example` and fill in the values.
Generate a JWT secret with:

    python -c "import secrets; print(secrets.token_hex(32))"

Load the product data:

    python -m scripts.seed_real_products

Frontend:

    cd frontend
    npm install

Create `frontend/.env` from `frontend/.env.example`.

## Run

    # terminal 1
    cd backend
    .\venv\Scripts\Activate.ps1
    uvicorn app.main:app --reload

    # terminal 2
    cd frontend
    npm run dev

Open http://localhost:5173

## API

| Method | URL | Auth |
|---|---|---|
| GET | /health, /health/db | no |
| POST | /signup, /login | no |
| GET | /me | yes |
| GET | /products, /products/search, /products/{slug} | yes |
| POST | /chatbot | yes |

## About the data

This is a learning/demo project. The Sasthra product information in
`backend/scripts/seed_real_products.py` was taken from the public Sasthra
websites and from an overview provided with the task. It is not official
company data. All product names and content belong to their owners.

To change the data, edit `backend/scripts/seed_real_products.py` and run
`python -m scripts.seed_real_products` again. No code changes are needed.

## Security notes

- Secrets live only in `backend/.env`, which is ignored by Git.
- The Gemini API key is never sent to the browser.
- Passwords are hashed with bcrypt. Login uses JWT with an expiry time.
- Login and chat requests are rate limited.
- Do not use `APP_ENV=development` in production (it enables /docs).

## Known limitations

- Search is keyword based, not meaning based.
- There is no chat history. Each message is handled on its own.
- Rate limiting is kept in memory and resets when the server restarts.
- Gemini can be slow or busy at times. The app retries and shows a safe message.