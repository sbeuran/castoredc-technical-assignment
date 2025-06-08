# Fruits API

A simple RESTful API for managing fruits, built with FastAPI and SQLite.

## Features

- Get all fruits
- Get a specific fruit by ID
- Add new fruits
- Persistent storage using SQLite
- Containerized application
- CI/CD pipeline with GitHub Actions

## Prerequisites

- Python 3.11+
- Docker (optional)

## Local Development Setup

1. Clone the repository:
```bash
git clone <repository-url>
cd fruits-api
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Unix/macOS
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run the application:
```bash
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`

## Running with Docker

1. Build the Docker image:
```bash
docker build -t fruits-api .
```

2. Run the container:
```bash
docker run -p 8000:8000 fruits-api
```

## API Documentation

Once the application is running, you can access:
- Interactive API documentation (Swagger UI): `http://localhost:8000/docs`
- Alternative API documentation (ReDoc): `http://localhost:8000/redoc`

### API Endpoints

#### GET /fruits
Returns all fruits in the database.

Response format:
```json
[
  {
    "id": 1,
    "fruit": "apple",
    "color": "red"
  }
]
```

#### GET /fruits/{fruit_id}
Returns a specific fruit by ID.

Response format:
```json
{
  "id": 1,
  "fruit": "apple",
  "color": "red"
}
```

#### POST /fruits
Adds a new fruit to the database.

Request body:
```json
{
  "fruit": "banana",
  "color": "yellow"
}
```

Response format:
```json
{
  "id": 2,
  "fruit": "banana",
  "color": "yellow"
}
```

## Testing

Run the tests using pytest:
```bash
pytest
```

## CI/CD Pipeline

The project includes a GitHub Actions workflow that:
1. Runs tests
2. Builds a Docker image
3. Pushes the image to GitHub Container Registry

## License

MIT 