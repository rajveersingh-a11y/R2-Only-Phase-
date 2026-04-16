import pandas as pd
from app.config import CSV_DIR

def map_final_phases(relation_map, labels, assignment):
    final_df = relation_map.copy()
    # Ensure consumer length matches labels
    # We assigned labels based on PCA features order.
    # relation_map might have different order
    # For robust pairing, we need to merge or map carefully
    
    # the labels are ordered by the consumer IDs in the PCA input (which is m_pivot.index)
    # Let's reconstruct
    pca_idx = pd.read_csv(CSV_DIR / "pca_features.csv")['consumer_id'].tolist()
    
    cluster_map = dict(zip(pca_idx, labels))
    final_df['kmeans_cluster'] = final_df['consumer_id'].map(cluster_map)
    final_df = final_df.dropna(subset=['kmeans_cluster']).copy()
    final_df['assigned_phase'] = final_df['kmeans_cluster'].map(assignment)
    
    final_df['phase_mapping_source'] = "K-Means+Minimization"
    final_df['confidence_score'] = 1.0 # Placeholder
    
    final_df.to_csv(CSV_DIR / "final_phase_mapping.csv", index=False)
    
    return final_df
