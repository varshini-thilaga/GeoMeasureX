from fastapi import APIRouter

router = APIRouter()

@router.get("/{id}/measurements")
def get_measurements(id: str, page: int = 1, page_size: int = 50):
    return {"page": page, "page_size": page_size, "total": 0, "results": []}
