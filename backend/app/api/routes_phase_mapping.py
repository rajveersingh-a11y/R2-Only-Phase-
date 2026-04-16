import os
from fastapi import APIRouter, HTTPException
from app.config import DATA_DIR, CSV_DIR
from app.schemas import PhaseMappingResponse
from app.services.excel_reader import load_data
from app.services.preprocessing import preprocess_data
from app.services.feature_engineering import engineer_features
from app.services.dimensionality_reduction import apply_pca
from app.services.clustering import run_kmeans
from app.services.optimization import assign_phases
from app.services.phase_mapper import map_final_phases
from app.services.evaluation import evaluate_mapping
from app.services.visualization import generate_plots

router = APIRouter()

@router.post("/run-phase-mapping", response_model=PhaseMappingResponse)
def run_phase_mapping(filename: str):
    file_path = DATA_DIR / filename
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="File not found")
    
    try:
        # Step 1 & 2: Read Excel and build relation
        meters_df, trans_df, gt_df = load_data(file_path)
        
        # Step 3 & 4: Extract, align, preprocess
        clean_M, clean_T, relation_map = preprocess_data(meters_df, trans_df, gt_df)
        
        # Step 5: Feature Engineering
        features_df = engineer_features(clean_M, clean_T, relation_map)
        
        # Step 6: PCA
        pca_df, explained_var = apply_pca(features_df)
        
        # Step 7: K-Means Clustering
        labels, centroids, metrics = run_kmeans(pca_df)
        
        # Step 8: Minimization Problem
        assignment, cost_matrix = assign_phases(clean_M, clean_T, relation_map, labels)
        
        # Step 9: Final Phase Labeling
        final_mapping_df = map_final_phases(relation_map, labels, assignment)
        
        # Evaluate & Visualize
        metrics = evaluate_mapping(final_mapping_df, gt_df, metrics, explained_var, pca_df)
        generate_plots(pca_df, labels, final_mapping_df, explained_var)
        
        consumers_processed = len(final_mapping_df)
        features_engineered = len(features_df.columns)
        
        return PhaseMappingResponse(
            message="Phase mapping pipeline completed successfully",
            consumers_processed=consumers_processed,
            features_engineered=features_engineered,
            pca_components=len(pca_df.columns),
            silhouette_score=metrics.get('silhouette_score', 0),
            davies_bouldin=metrics.get('davies_bouldin', 0),
            cluster_counts={str(k): int(v) for k, v in final_mapping_df['kmeans_cluster'].value_counts().items()},
            phase_counts={str(k): int(v) for k, v in final_mapping_df['assigned_phase'].value_counts().items()}
        )
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))
