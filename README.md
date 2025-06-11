# Fruits API

A simple RESTful API for managing fruits, built with FastAPI and SQLite, with a modern Next.js frontend.

## Features

- Get all fruits
- Get a specific fruit by ID
- Persistent storage using SQLite
- Containerized application
- CI/CD pipeline with GitHub Actions
- Modern Next.js frontend with Material UI

## Prerequisites

- Python 3.11+
- Node.js 18+
- Docker (optional)

## Local Development Setup

1. Clone the repository:
```bash
git clone <repository-url>
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

4. Run the backend application:
```bash
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`

5. Run the frontend application:
```bash
cd fruits-frontend
npm install
npm run dev
```

The frontend will be available at `http://localhost:3000`

## Running with Docker

1. Build the Docker image:
```bash
docker build -t fruits-api .
```

2. Run the container:
```bash
docker run -p 8000:8000 fruits-api
```

### API Endpoints

#### GET /api/v1/fruits
Returns all fruits in the database.

![Get All Fruits](docs/postman-get-all-fruits.png)

#### GET /api/v1/fruits/{fruit_id}
Returns a specific fruit by ID.

![Get Specific Fruit](docs/postman-get-specific-fruit.png)

#### GET /api/v1/data
Returns all data including fruits, suppliers, and nutritional information.

![Get All Data](docs/postman-get-all-data.png)

Example response:
```json
{
    "fruits": [
        {
            "id": 1,
            "name": "Apple",
            "color": "Red",
            "taste": "Sweet",
            "origin_country": "USA",
            "price_per_kg": 2.99,
            "suppliers": [
                {
                    "id": 1,
                    "name": "Fresh Farms",
                    "contact_email": "contact@freshfarms.com",
                    "country": "USA",
                    "rating": 4.5
                }
            ],
            "nutritional_info": {
                "id": 1,
                "calories": 52,
                "carbohydrates": 14.0,
                "protein": 0.3,
                "fat": 0.2,
                "fiber": 2.4,
                "vitamins": "A, C"
            }
        },
        {
            "id": 2,
            "name": "Banana",
            "color": "Yellow",
            "taste": "Sweet",
            "origin_country": "Ecuador",
            "price_per_kg": 1.99,
            "suppliers": [
                {
                    "id": 3,
                    "name": "Tropical Exports",
                    "contact_email": "sales@tropicalexports.com",
                    "country": "Ecuador",
                    "rating": 4.2
                }
            ],
            "nutritional_info": {
                "id": 2,
                "calories": 89,
                "carbohydrates": 23.0,
                "protein": 1.1,
                "fat": 0.3,
                "fiber": 2.6,
                "vitamins": "B6, C"
            }
        },
        {
            "id": 3,
            "name": "Orange",
            "color": "Orange",
            "taste": "Sweet-Citrus",
            "origin_country": "Spain",
            "price_per_kg": 3.49,
            "suppliers": [
                {
                    "id": 2,
                    "name": "Global Fruits Co",
                    "contact_email": "info@globalfruits.com",
                    "country": "Spain",
                    "rating": 4.8
                }
            ],
            "nutritional_info": {
                "id": 3,
                "calories": 47,
                "carbohydrates": 12.0,
                "protein": 0.9,
                "fat": 0.1,
                "fiber": 2.4,
                "vitamins": "C"
            }
        }
    ],
    "total_fruits": 3,
    "total_suppliers": 3,
    "total_nutritional_records": 3
}
```

## Frontend Application

The frontend application is built with Next.js and Material UI, featuring:
- Modern dark theme
- Interactive data grid with sorting and filtering
- CSV export functionality
- Detailed view with extended data
- Country flags and tooltips

Demo video: [Video Demo](docs/video-demo.mov)

## Azure Resources

The application is deployed using Azure resources:

![Azure Resources](docs/azure-resources.png)

## CI/CD Pipeline

The project uses GitHub Actions for continuous integration and deployment:

1. Backend Pipeline (`main.yml`):
   - Triggers on:
     - Push to main branch (excluding frontend and markdown files)
     - Pull request events
     - Manual workflow dispatch
   - Pipeline steps:
     - Sets up Python 3.11
     - Installs dependencies
     - Runs tests
     - Configures Azure App Service
     - Deploys to Azure App Service
     - Streams deployment logs
     - Performs health check verification

2. Frontend Pipeline (`frontend.yml`):
   - Triggers on:
     - Push to main branch (frontend directory changes)
     - Pull request events
     - Manual workflow dispatch
   - Pipeline steps:
     - Sets up Node.js 18
     - Installs dependencies
     - Builds Next.js application
     - Copies static web app configuration
     - Deploys to Azure Static Web Apps

### Manual Deployment

Both pipelines support manual triggering through GitHub Actions:
1. Navigate to the "Actions" tab in GitHub
2. Select either "Backend CI/CD Pipeline" or "Frontend CI/CD Pipeline"
3. Click "Run workflow"
4. Select the branch (usually 'main')
5. Click "Run workflow"

## Production URLs

- Backend API: https://fruits-api-app.azurewebsites.net
- Frontend Application: https://delightful-beach-03aa35903.6.azurestaticapps.net

## License

MIT 