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
