# My Studienkolleg 
Contains both frontend and backend

## Requirements
- python 3.12
- node 23.3.0
- docker
- MongoDB Docker image (community edition. For more details see: [Docker installation Guide](https://www.mongodb.com/docs/manual/tutorial/install-mongodb-community-with-docker/))

## How to run 
1. Get Docker Image
```
docker pull mongodb/mongodb-community-server:latest
docker run --name mongodb -p 27017:27017 -d mongodb/mongodb-community-server:latest
```
3. Run Backend (in one terminal)
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
