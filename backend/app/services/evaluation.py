import pandas as pd
import numpy as np
from app.config import CSV_DIR

def evaluate_mapping(final_mapping_df, gt_df, metrics, explained_var, pca_df):
    final_metrics = []
    
    final_metrics.append({"Metric": "total_consumers_processed", "Value": len(final_mapping_df)})
    final_metrics.append({"Metric": "pca_components_retained", "Value": len(pca_df.columns)})
    final_metrics.append({"Metric": "silhouette_score", "Value": metrics.get('silhouette_score', 0)})
    final_metrics.append({"Metric": "davies_bouldin_index", "Value": metrics.get('davies_bouldin', 0)})
    final_metrics.append({"Metric": "calinski_harabasz_score", "Value": metrics.get('calinski_harabasz', 0)})
    
    p_counts = final_mapping_df['assigned_phase'].value_counts()
    for p in ['A', 'B', 'C']:
        final_metrics.append({"Metric": f"final_phase_count_{p}", "Value": p_counts.get(p, 0)})
        
    df_metrics = pd.DataFrame(final_metrics)
    df_metrics.to_csv(CSV_DIR / "evaluation_metrics.csv", index=False)
    
    return {row['Metric']: row['Value'] for _, row in df_metrics.iterrows()}
