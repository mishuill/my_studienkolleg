# My Studienkolleg 
Contains both frontend and backend


## How to run 
1. Run Backend (in one terminal)
```
cd my_sk_api/
pip install -r requirements.txt
export $(cat ../.env | xargs)
fastapi run
```

2. Run Frontend (in another terminal)
```
cd my_sk_frontend/
npm install
npm run dev
```
