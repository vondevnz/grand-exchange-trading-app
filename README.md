# Grand Exchange Trading App

## Backend (FastAPI)
cd grand-exchange-trading-app 
docker-compose up --build   
docker-compose exec app python -m app.scripts.pollingData

## Frontend (React + Vite)
cd frontend    
npm install      
npm run dev         