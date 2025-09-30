# 🤖 AI Interview Coach

An AI-powered web application that helps students and professionals practice technical interviews.  
Users can log in, select scenarios, answer questions, and receive **real-time AI feedback** powered by Gemini.  

---

## 🚀 Features

- **Authentication** – Register and log in with JWT-based authentication.  
- **Admin Panel** – Seed and manage interview scenarios.  
- **Interview Sessions**  
  - Start interview sessions for a given role/scenario.  
  - Answer technical questions.  
  - Get AI-generated feedback & scores.  
  - View a **session summary** (strengths, improvements, averages).  
- **User Dashboard**  
  - Profile overview.  
  - Quick access to My Sessions & My Attempts.  
- **Frontend** – Vue 3 + Tailwind UI with a clean, professional design.  
- **Backend** – FastAPI with SQLModel + PostgreSQL.  
- **Dockerized** – Full project runs with `docker-compose`.  

---

## 🛠️ Tech Stack

### Backend
- [FastAPI](https://fastapi.tiangolo.com/)  
- [SQLModel](https://sqlmodel.tiangolo.com/)  
- [PostgreSQL](https://www.postgresql.org/)  
- JWT Authentication  
- Gemini API for AI feedback  

### Frontend
- [Vue 3](https://vuejs.org/)  
- [Vue Router](https://router.vuejs.org/)  
- [Axios](https://axios-http.com/)  
- [Tailwind CSS](https://tailwindcss.com/)  

### DevOps
- [Docker](https://www.docker.com/) & Docker Compose  

---

## 📂 Project Structure

ai-interview-coach/
│
├── backend/ # FastAPI backend
│ ├── app/
│ │ ├── routers/ # API routes (auth, interview, scenarios, etc.)
│ │ ├── models.py # Database models
│ │ ├── database.py # DB connection
│ │ ├── deps.py # Auth/session helpers
│ │ └── security.py # JWT + password hashing
│ └── Dockerfile
│
├── frontend/ # Vue 3 frontend
│ ├── src/
│ │ ├── pages/ # Vue pages (Login, Register, Dashboard, etc.)
│ │ ├── components/ # Navbar, UI components
│ │ ├── lib/ # Axios wrapper, auth utils
│ │ └── main.js
│ └── Dockerfile
│
├── docker-compose.yml # Orchestrates backend + frontend + db
├── .env # Environment variables
└── README.md # Project documentation



---

## ⚙️ Setup & Installation

### 1. Clone the repo
```bash
git clone https://github.com/<your-username>/ai-interview-coach.git
cd ai-interview-coach

2. Configure environment variables
Create a .env file in root with:
# Backend
DATABASE_URL=postgresql+psycopg2://coach:coachpass@db:5432/coachdb
GEMINI_API_KEY=your_google_gemini_key
SECRET_KEY=your_secret
ACCESS_TOKEN_EXPIRE_MINUTES=120
ALGORITHM=HS256
ADMIN_EMAIL=admin@example.com

# Frontend
VITE_API_BASE_URL=http://localhost:8000


3. Run with Docker
docker-compose up --build
Backend: http://localhost:8000
Frontend: http://localhost:5173

