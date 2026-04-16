import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

DATA_DIR = BASE_DIR / "data"
OUTPUTS_DIR = BASE_DIR / "outputs"

CSV_DIR = OUTPUTS_DIR / "csv"
PLOTS_DIR = OUTPUTS_DIR / "plots"
MODELS_DIR = OUTPUTS_DIR / "models"

# Create directories if they don't exist
DATA_DIR.mkdir(parents=True, exist_ok=True)
OUTPUTS_DIR.mkdir(parents=True, exist_ok=True)
CSV_DIR.mkdir(parents=True, exist_ok=True)
PLOTS_DIR.mkdir(parents=True, exist_ok=True)
MODELS_DIR.mkdir(parents=True, exist_ok=True)

class Settings:
    PCA_COMPONENTS = 0.95
    KMEANS_CLUSTERS = 3
    RANDOM_STATE = 42

settings = Settings()
