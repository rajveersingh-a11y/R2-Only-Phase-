import os
import shutil
from fastapi import APIRouter, UploadFile, File, HTTPException
from app.config import DATA_DIR
from app.schemas import UploadResponse

router = APIRouter()

@router.post("/upload", response_model=UploadResponse)
async def upload_file(file: UploadFile = File(...)):
    if not file.filename.endswith(".xlsx"):
        raise HTTPException(status_code=400, detail="Only .xlsx files are supported")
    
    file_path = DATA_DIR / file.filename
    try:
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        return UploadResponse(filename=file.filename, message="File uploaded successfully")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
