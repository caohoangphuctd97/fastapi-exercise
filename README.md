# fastapi-exercise

This is a FastAPI application that provides a simple user management system with post creation and deletion functionality.

## Setup Instructions

### Start the MySQL service

Run the following command to start the MySQL service in detached mode:
```bash
docker-compose -f deployments/docker-compose.yml up mysql -d
```

### Create .env file

Create a .env file in the root directory with the following content:
```bash
DATABASE_USERNAME=mysql
DATABASE_NAME=mysql
DATABASE_PASSWORD=mysql
DATABASE_HOST=localhost
```

### Run migrations

Run the following command to apply the database migrations:
```bash
alembic upgrade head
```

### Build and run the application

Build the Docker image and start the application with the following command:
```bash
docker-compose -f deployments/docker-compose.yml up --build
```

## API Endpoints

The application provides the following API endpoints:

- `POST /signup`: Register a new user.
- `POST /login`: Authenticate a user.
- `POST /post`: Create a new post.
- `GET /post`: Retrieve all posts of the authenticated user.
- `DELETE /post/{post_id}`: Delete a post by its ID.

For more details about the request and response formats, refer to the Swagger UI at `http://localhost:80/api/v1/docs`.