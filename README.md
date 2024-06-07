# fastapi-exercise
# Setup Instructions
Run the following command to start the MySQL service in detached mode:
```bash
docker-compose -f deployments/docker-compose.yml -p queue up mysql -d
```
Create env file:
```bash
DATABASE_USERNAME=mysql
DATABASE_NAME=mysql
DATABASE_PASSWORD=mysql
DATABASE_HOST=localhost
```

Run code:
```bash
dotenv run uvicorn app.main:app --reload
```
Then Open http://127.0.0.1:8000/api/v1/docs