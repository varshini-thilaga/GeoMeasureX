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
