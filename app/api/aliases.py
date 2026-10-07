from fastapi import APIRouter
from app.api.v1.files import upload_file, get_file

router = APIRouter()

@router.post("/")
async def upload_file_alias(file, repair: bool = False, assume_crs: str = None):
    return await upload_file(file, repair, assume_crs)

@router.get("/{id}")
def get_file_alias(id: str):
    return get_file(id)
