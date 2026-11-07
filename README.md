# DevTracker — Full-Stack Project Monitoring & Task Analytics Dashboard

DevTracker is a production-grade, asynchronous full-stack web application designed to track software development tasks and project builds.

# Live Application: https://devtracker-whuu.vercel.app/


#Tech Stack

- Frontend Client: React.js ,Context State Hooks, Responsive Bootstrap framework.
- Asynchronous Backend: Python, FastAPI.
- Relational Storage: PostgreSQL Database.
- Database ORM: SQLAlchemy 2.0 Asynchronous ORM utilizing the `asyncpg`.
- Security & Session Layer: Stateless JSON Web Token (JWT) session authorization and `Bcrypt` cryptographic password hashing context handlers.
- Cloud Infrastructure: Render (Backend API + Database) and Vercel (Frontend).


# Project Repository Tree

devtracker/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── auth.py          # Bcrypt hashing & JWT token verification modules
│   │   ├── database.py      # SQLAlchemy 2.0 Async engine connection setups
│   │   ├── main.py          # FastAPI application routes & CORS policies
│   │   ├── models.py        # Relational PostgreSQL database tables schemas
│   │   └── schemas.py       # Pydantic input/output parsing structures
│   └── requirements.txt     # Python production-grade dependencies
└── frontend/
    ├── src/
    │   ├── api.js           # Central Axios connection instance mapping
    │   ├── App.jsx          # Main application wrapper and state manager
    │   ├── Auth.jsx         # Stateless login/signup form interface components
    │   ├── Dashboard.jsx    # Real-time analytics counter grid & CRUD work ledger view
    │   ├── index.css        # Premium Light-theme application global styling parameters
    │   └── main.jsx         # React mounting injection node entry point
    ├── index.html
    └── package.json         # Node.js production ecosystem packages


# Local Machine Setup & Installation

To run this full-stack product locally on your machine, follow these instructions:

#1. Database Setup
Ensure you have a local PostgreSQL engine running via pgAdmin. Create a fresh empty database called `devtracker`.

#2. Backend Engine Run

# Navigate to the backend directory
cd backend

# Install verified stable dependencies
pip install -r requirements.txt

# Execute the local server reload watch pipeline
uvicorn app.main:app --reload

The local API interface will switch live on `http://127.0.0.1:8000`.

#3. Frontend Client Run

# Navigate to the frontend directory
cd frontend

# Install node dependencies
npm install

# Start the local React client compiler tool
npm run dev

Open `http://localhost:5173` inside your browser client to test local workflows.

