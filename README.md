# Insurance Claims Management & Risk Analysis API

A simple, JSON-backed REST API built with FastAPI to manage policyholders and claims, perform basic analytics and reporting, and persist data in flat JSON files. Ideal as an internship exercise or lightweight prototype.

---

## Features

- **Policyholder Management**  
  - Create and list policyholders  
- **Claim Management**  
  - Create and list claims  
- **Analytics**  
  - Claim frequency per policyholder  
  - Identify high-risk policyholders  
  - Aggregate claims by policy type  
- **Reporting**  
  - Monthly claims count  
  - Average claim amount by policy type  
  - Highest claim of all time  
  - Pending claims list  
- **API Docs**  
  - Interactive Swagger UI at `/docs`  
  - ReDoc at `/redoc`  

---

## Tech Stack

- **Python** ≥ 3.9  
- **FastAPI** (latest stable)  
- **Uvicorn** ASGI server  
- **Pydantic V2** for schemas & validation  
- **JSON files** for persistence (`/data/*.json`)  
- **pytest** for unit tests  
- **Docker** (optional)  

---

## Prerequisites

- Python 3.9+  
- pip (or pipenv/poetry)  
- (Optional) Docker & Docker Compose  

---

## Installation & Setup

1. **Clone the repo**  
   ```bash
   git clone <your-repo-url>.git
   cd insurance-claims-api```
   
2. install dependencies
  ```bash
  pip install --no-cache-dir -r requirements.txt ```

  Running Locally
  ``bash
  uvicorn app.main:app --reload```

  Open your browser at http://localhost:8000/docs 
  for Swagger UI, or http://localhost:8000/redoc for ReDoc.

3. Running Tests
  ```bash
  pytest -q
  ```

4. Docker

  Build the Docker image:
  ``bash
  docker build -t insurance-api .

  ```
  Run the container:
  ```bash
  docker run -it --rm -p 8000:8000 insurance-api
  ```


## API Documentation
Swagger UI:
```bash GET http://localhost:8000/docs
```
ReDoc:
```bash GET http://localhost:8000/redoc```