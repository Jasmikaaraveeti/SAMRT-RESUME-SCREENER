# Smart Resume Screener

A modern, full-stack AI-powered resume screening platform.

## Features
- AI Resume Parsing & Scoring
- Multi-tenant Google OAuth Authentication
- Detailed Analytics Dashboard
- Responsive SaaS Design

## Google OAuth Setup
To enable real Google Sign-In:
1. Go to the [Google Cloud Console](https://console.cloud.google.com/).
2. Create a new Project.
3. Navigate to **APIs & Services** > **Credentials**.
4. Click **Create Credentials** > **OAuth client ID**.
5. Set Application Type to **Web application**.
6. Under **Authorized redirect URIs**, add `http://localhost:8000/api/auth/google/callback`.
7. Copy the **Client ID** and **Client Secret**.
8. Create a `.env` file in the `backend/` directory based on `backend/.env.example` and fill in your credentials.

## Running Locally
1. Start Backend: `cd backend && .\venv\Scripts\python -m uvicorn main:app --host 0.0.0.0 --port 8000`
2. Start Frontend: `cd frontend && npm run dev`
3. Access: `http://localhost:5173`
