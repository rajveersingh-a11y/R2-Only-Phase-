# Phase Mapping Project

## Overview
A full-stack application to perform Phase Mapping (identifying A, B, C phases) from smart meter voltage data.
The solution utilizes an unsupervised learning approach: Feature Engineering -> PCA -> K-Means Clustering -> Minimization problem (Hungarian Algorithm) for phase assignment.

## Folder Structure
- `backend/`: FastAPI backend for running the data processing pipeline.
- `frontend/`: React + Vite frontend dashboard.

## Methodology
1. **Preprocessing**: Extract and align time series, impute missing values.
2. **Feature Engineering**: Generate statistical, temporal, and transformer-relative features from voltage profiles.
3. **PCA**: Reduce dimensions while retaining 95% variance.
4. **K-Means Clustering**: Group consumers into 3 clusters.
5. **Minimization-based Bijection**: Use the Hungarian Algorithm to enforce a 1-to-1 mapping between the 3 clusters and physical phases A, B, and C.

## Installation & Running

### Backend
1. Go to `backend/` directory.
2. Install requirements: `pip install -r requirements.txt`
3. Run the server: `python run.py` (Server runs on http://localhost:8000)

### Frontend
1. Go to `frontend/` directory.
2. Install dependencies: `npm install`
3. Run the dev server: `npm run dev`

Upload `sample_grid_data_3phase.xlsx` via the frontend dashboard to run the pipeline.
