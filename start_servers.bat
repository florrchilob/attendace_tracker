@echo off
start cmd /k "cd frontend && npm run dev -- --port 80"
start cmd /k "cd backend && python app.py" 