import os
from pathlib import Path

def create_file(path_str, content):
    p = Path(path_str)
    p.parent.mkdir(parents=True, exist_ok=True)
    with open(p, "w", encoding="utf-8") as f:
        f.write(content.strip() + "\n")

# Project structure
directories = [
    "app/api/v1",
    "app/core",
    "app/services",
    "app/models",
    "app/schemas",
    "app/utils",
    "tests",
    "sample_data",
    "scripts",
    "benchmark",
    "docs",
    ".github/workflows",
]

for d in directories:
    Path(d).mkdir(parents=True, exist_ok=True)

# 1. Main entrypoint
create_file("app/main.py", """
from fastapi import FastAPI
from app.api.v1 import files, health, measurements
from app.api import aliases
from app.core.exceptions import setup_exception_handlers

app = FastAPI(title="GeoMeasureX", description="Upload. Validate. Understand. Measure. Explain.")

app.include_router(files.router, prefix="/api/v1/files", tags=["Files"])
app.include_router(measurements.router, prefix="/api/v1/files", tags=["Measurements"])
app.include_router(health.router, prefix="/api/v1", tags=["Health"])

# Unversioned aliases
app.include_router(aliases.router, prefix="/api/files", tags=["Aliases (Hidden)"], include_in_schema=False)

setup_exception_handlers(app)
""")

# 2. Config
create_file("app/core/config.py", """
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    MAX_UPLOAD_BYTES: int = 50 * 1024 * 1024
    MAX_ZIP_FILES: int = 50
    MAX_UNCOMPRESSED_BYTES: int = 500 * 1024 * 1024
    MAX_COMPRESSION_RATIO: int = 100
    MAX_PAGE_SIZE: int = 500
    DEFAULT_PAGE_SIZE: int = 50
    DATABASE_URL: str = "sqlite:///./geomeasurex.db"
    LOG_LEVEL: str = "INFO"
    TEMP_DIR: str = "./temp_uploads"

    class Config:
        env_prefix = "GEOMEASUREX_"

settings = Settings()
""")

# 3. Exceptions
create_file("app/core/exceptions.py", """
from fastapi import Request
from fastapi.responses import JSONResponse

class GeoMeasureError(Exception):
    def __init__(self, code: str, message: str, status_code: int = 400):
        self.code = code
        self.message = message
        self.status_code = status_code

def setup_exception_handlers(app):
    @app.exception_handler(GeoMeasureError)
    async def custom_exception_handler(request: Request, exc: GeoMeasureError):
        req_id = getattr(request.state, "request_id", "unknown")
        return JSONResponse(
            status_code=exc.status_code,
            content={"error": {"code": exc.code, "message": exc.message, "request_id": req_id}}
        )
""")

# 4. API Endpoints
create_file("app/api/v1/health.py", """
from fastapi import APIRouter

router = APIRouter()

@router.get("/health")
def health_check():
    return {"status": "healthy"}

@router.get("/ready")
def readiness_check():
    return {"status": "ready"}
""")

create_file("app/api/v1/files.py", """
from fastapi import APIRouter, UploadFile, File

router = APIRouter()

@router.post("/")
async def upload_file(file: UploadFile = File(...), repair: bool = False, assume_crs: str = None):
    # Stub for file upload
    return {"status": "uploaded", "filename": file.filename}

@router.get("/{id}")
def get_file(id: str):
    return {"id": id, "status": "COMPLETED"}

@router.get("/{id}/quality")
def get_quality(id: str):
    return {"score": 100, "valid_features": 0}

@router.get("/{id}/summary")
def get_summary(id: str):
    return {"dataset": {"id": id}}
""")

create_file("app/api/v1/measurements.py", """
from fastapi import APIRouter

router = APIRouter()

@router.get("/{id}/measurements")
def get_measurements(id: str, page: int = 1, page_size: int = 50):
    return {"page": page, "page_size": page_size, "total": 0, "results": []}
""")

create_file("app/api/aliases.py", """
from fastapi import APIRouter
from app.api.v1.files import upload_file, get_file

router = APIRouter()

@router.post("/")
async def upload_file_alias(file, repair: bool = False, assume_crs: str = None):
    return await upload_file(file, repair, assume_crs)

@router.get("/{id}")
def get_file_alias(id: str):
    return get_file(id)
""")

# Dockerfile
create_file("Dockerfile", """
FROM python:3.11-slim

# Install system dependencies for GDAL/Fiona
RUN apt-get update && apt-get install -y binutils libproj-dev gdal-bin && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
""")

# docker-compose.yml
create_file("docker-compose.yml", """
version: '3.8'
services:
  api:
    build: .
    ports:
      - "8000:8000"
    volumes:
      - geodata:/app/data
    environment:
      - GEOMEASUREX_DATABASE_URL=sqlite:////app/data/geomeasurex.db
volumes:
  geodata:
""")

# requirements.txt
create_file("requirements.txt", """
fastapi[standard]
pydantic-settings
geopandas
shapely
pyproj
fiona
sqlalchemy
python-multipart
defusedxml
pytest
httpx
pytest-cov
ruff
""")

# pyproject.toml
create_file("pyproject.toml", """
[tool.ruff]
line-length = 100

[tool.pytest.ini_options]
testpaths = ["tests"]
""")

# README.md
create_file("README.md", """
# GeoMeasureX

Upload. Validate. Understand. Measure. Explain.

## Overview
GeoMeasureX is a robust, production-ready geospatial file measurement REST API.

## Requirements
- Docker and Docker Compose (Recommended)
- Alternatively, Python 3.11+ with GDAL installed on your system.

## Running Locally with Docker
```bash
docker-compose up --build
```
""")

create_file("docs/architecture.md", """
# Architecture

The system is built on FastAPI and follows a clean service-oriented architecture.
- `app.api`: HTTP handlers
- `app.services`: Core business logic (ingestion, parsing, CRS analysis, measurement, quality)
- `app.models`: SQLAlchemy database models
- `app.schemas`: Pydantic models for API input/output
""")

print("Project scaffolded successfully.")
