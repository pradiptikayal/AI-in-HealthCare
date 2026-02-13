# Start the MVP - Quick Instructions

## Option 1: Manual Start (Recommended)

### Terminal 1 - Backend
```bash
cd backend
python app.py
```

Wait for: `Running on http://127.0.0.1:5000`

### Terminal 2 - Frontend
```bash
cd frontend
npm run dev
```

Wait for: `Local: http://localhost:3000`

### Open Browser
Go to: `http://localhost:3000`

## Option 2: Windows PowerShell Script

Save this as `start-mvp.ps1`:

```powershell
# Start Backend
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd backend; python app.py"

# Wait a moment for backend to start
Start-Sleep -Seconds 3

# Start Frontend
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd frontend; npm run dev"

# Wait a moment then open browser
Start-Sleep -Seconds 5
Start-Process "http://localhost:3000"
```

Then run:
```powershell
.\start-mvp.ps1
```

## What You Should See

### Backend Terminal
```
 * Serving Flask app 'app'
 * Debug mode: on
WARNING: This is a development server.
 * Running on http://127.0.0.1:5000
```

### Frontend Terminal
```
VITE v5.0.8  ready in 500 ms

  ➜  Local:   http://localhost:3000/
  ➜  Network: use --host to expose
  ➜  press h + enter to show help
```

### Browser
- Registration page should load
- Clean, purple gradient background
- White form card in the center

## First Time Setup Checklist

Before starting, make sure you've done:

- [ ] Installed Python 3.8+
- [ ] Installed Node.js 14+
- [ ] Ran `pip install -r requirements.txt` in backend folder
- [ ] Ran `npm install` in frontend folder
- [ ] Created backend/data directory (should exist already)

## Quick Test

1. Register a new patient
2. Login with those credentials
3. Submit an assessment with symptoms: "headache, fever"
4. View your prescription
5. Return to dashboard to see history

## Troubleshooting

### Port Already in Use

**Backend (Port 5000):**
```bash
# Windows
netstat -ano | findstr :5000
taskkill /PID <PID> /F
```

**Frontend (Port 3000):**
```bash
# Windows
netstat -ano | findstr :3000
taskkill /PID <PID> /F
```

### Backend Errors

If you see import errors:
```bash
cd backend
pip install -r requirements.txt
```

### Frontend Errors

If you see module errors:
```bash
cd frontend
rm -rf node_modules
npm install
```

### CORS Errors

Make sure:
1. Backend is running on port 5000
2. Frontend is running on port 3000
3. Both are running simultaneously

## Stop the Servers

Press `Ctrl+C` in each terminal window to stop the servers.

## Ready to Go!

Once both servers are running, you have a fully functional Patient Assessment System MVP! 🎉

See MVP-GUIDE.md for detailed usage instructions and API documentation.
