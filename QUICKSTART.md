# Quick Start Guide

## Prerequisites
- Python 3.13.5 (installed ✓)
- Node.js (installed ✓)
- npm (installed ✓)

## Backend Setup (Already Completed)

The backend is ready to run:

```bash
cd backend
python app.py
```

The API will be available at `http://localhost:5000`

## Frontend Setup (Already Completed)

The frontend is ready to run:

```bash
cd frontend
npm run dev
```

The application will be available at `http://localhost:3000`

## What's Been Set Up

### Backend
- ✓ Python virtual environment created (`backend/venv/`)
- ✓ Flask installed with CORS support
- ✓ Testing frameworks installed (pytest + Hypothesis)
- ✓ Password hashing (bcrypt) and JWT authentication libraries
- ✓ Basic Flask app with health check endpoint
- ✓ pytest configuration

### Frontend
- ✓ React 18 with Vite build tool
- ✓ React Router for navigation
- ✓ Axios for API calls
- ✓ Testing libraries (Vitest + React Testing Library + fast-check)
- ✓ Vite proxy configured to forward `/api` requests to backend
- ✓ Basic React app structure

### Project Structure
```
patient-assessment-system/
├── backend/
│   ├── venv/              # Python virtual environment
│   ├── tests/             # Backend tests
│   ├── app.py             # Flask application
│   ├── requirements.txt   # Python dependencies
│   ├── pytest.ini         # pytest configuration
│   └── .env.example       # Environment variables template
├── frontend/
│   ├── node_modules/      # Node dependencies
│   ├── src/
│   │   ├── main.jsx       # React entry point
│   │   ├── App.jsx        # Main App component
│   │   ├── index.css      # Global styles
│   │   └── test/          # Frontend tests
│   ├── index.html         # HTML template
│   ├── package.json       # Node dependencies
│   └── vite.config.js     # Vite configuration
├── .gitignore             # Git ignore rules
├── README.md              # Full documentation
└── QUICKSTART.md          # This file
```

## Next Steps

You're ready to start implementing features! The next task in the implementation plan is:

**Task 2: Implement JSON-based data storage**
- Create data directory and JSON files
- Implement data access utilities
- Initialize sample doctor data

## Testing

### Run Backend Tests
```bash
cd backend
pytest
```

### Run Frontend Tests
```bash
cd frontend
npm test
```

## Verify Installation

### Test Backend
```bash
cd backend
python app.py
```
Then visit `http://localhost:5000/api/health` - you should see:
```json
{"status": "ok", "message": "Patient Assessment System API is running"}
```

### Test Frontend
```bash
cd frontend
npm run dev
```
Then visit `http://localhost:3000` - you should see the Patient Assessment System welcome page.

## Environment Configuration

Before running in production, create a `.env` file in the backend directory:

```bash
cd backend
cp .env.example .env
```

Then edit `.env` and set secure values for:
- `SECRET_KEY`
- `JWT_SECRET_KEY`

## Troubleshooting

### Backend Issues
- Make sure the virtual environment is activated before running
- Windows: `venv\Scripts\activate`
- macOS/Linux: `source venv/bin/activate`

### Frontend Issues
- If you see Node version warnings, they're just warnings - the app will still work
- Clear node_modules and reinstall if needed: `rm -rf node_modules && npm install`

### Port Conflicts
- Backend uses port 5000 (change in `app.py` if needed)
- Frontend uses port 3000 (change in `vite.config.js` if needed)
