# Architecture

The system is built on FastAPI and follows a clean service-oriented architecture.
- `app.api`: HTTP handlers
- `app.services`: Core business logic (ingestion, parsing, CRS analysis, measurement, quality)
- `app.models`: SQLAlchemy database models
- `app.schemas`: Pydantic models for API input/output
