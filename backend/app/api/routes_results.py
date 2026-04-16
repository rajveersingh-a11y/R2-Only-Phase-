import os
import io
import pandas as pd
from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse, JSONResponse
from app.config import CSV_DIR, PLOTS_DIR

router = APIRouter()

@router.get("/results/summary")
def get_summary():
    metrics_path = CSV_DIR / "evaluation_metrics.csv"
    if not metrics_path.exists():
        raise HTTPException(status_code=404, detail="Metrics not found")
    df = pd.read_csv(metrics_path)
    metrics = {row['Metric']: row['Value'] for _, row in df.iterrows()}
    return {"metrics": metrics}

@router.get("/results/download/{filename}")
def download_result(filename: str):
    if filename.endswith(".csv"):
        file_path = CSV_DIR / filename
    elif filename.endswith(".png"):
        file_path = PLOTS_DIR / filename
    else:
        raise HTTPException(status_code=400, detail="Invalid file type")
    
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="File not found")
        
    return FileResponse(file_path, filename=filename)
