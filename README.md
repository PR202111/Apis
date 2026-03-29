# API Project

This project is a FastAPI application with a PostgreSQL database, running entirely in Docker.

## Table of Contents

- [Requirements](#requirements)
- [Setup](#setup)
- [Running the Project](#running-the-project)
- [Accessing the Database](#accessing-the-database)
- [Docker Notes](#docker-notes)
- [Project Structure](#project-structure)

---

## Requirements

- [Docker](https://www.docker.com/get-started)  
- [Docker Compose](https://docs.docker.com/compose/install/)  
- Optional: `psql` client (if you want to connect from host machine)

---

## Setup

1. Clone the repository:

```bash
git clone <your-repo-url>
cd <your-repo-folder>
```

2. Build and start the containers:

```bash
docker-compose up --build
```

This will start:

- `api-api` (FastAPI server)  
- `api-db` (PostgreSQL database)  

---

## Running the Project

Once the containers are running:

- FastAPI server: http://localhost:8000  
- It will automatically reload on code changes.

You can stop the containers with:

```bash
docker-compose down
```

---

## Accessing the Database

### From inside the API container:

```bash
docker exec -it api-api bash
psql -h api-db -U postgres -d mydatabase
```

### From your local machine (optional, requires port mapping):

```bash
psql -h localhost -U postgres -d mydatabase
```

Tables:

```sql
\dt;
```

Sample query:

```sql
SELECT * FROM users;
```

---

## Docker Notes

- Containers communicate using **Docker network**, using service names (like `api-db`) as hostnames.  
- Port mapping (`5432:5432`) is only needed if you want to access Postgres from your host machine.  
- Database initialization is handled automatically on first startup.

---

## Project Structure

```
.
├── app/                # FastAPI application code
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── README.md
```

---


