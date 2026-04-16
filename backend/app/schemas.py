from pydantic import BaseModel
from typing import List, Dict, Optional, Any

class UploadResponse(BaseModel):
    filename: str
    message: str

class PhaseMappingResponse(BaseModel):
    message: str
    consumers_processed: int
    features_engineered: int
    pca_components: int
    silhouette_score: float
    davies_bouldin: float
    cluster_counts: Dict[str, int]
    phase_counts: Dict[str, int]

class SummaryMetrics(BaseModel):
    metrics: Dict[str, Any]
