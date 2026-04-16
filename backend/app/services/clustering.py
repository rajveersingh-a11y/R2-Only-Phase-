import pandas as pd
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score, davies_bouldin_score, calinski_harabasz_score
from app.config import settings, CSV_DIR

def run_kmeans(pca_df):
    kmeans = KMeans(n_clusters=settings.KMEANS_CLUSTERS, random_state=settings.RANDOM_STATE)
    labels = kmeans.fit_predict(pca_df)
    
    out_df = pd.DataFrame({"consumer_id": pca_df.index, "kmeans_cluster": labels}).set_index("consumer_id")
    out_df.to_csv(CSV_DIR / "kmeans_labels.csv")
    
    metrics = {
        "silhouette_score": silhouette_score(pca_df, labels),
        "davies_bouldin": davies_bouldin_score(pca_df, labels),
        "calinski_harabasz": calinski_harabasz_score(pca_df, labels)
    }
    
    return labels, kmeans.cluster_centers_, metrics
