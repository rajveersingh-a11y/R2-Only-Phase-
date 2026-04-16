import pandas as pd
from sklearn.decomposition import PCA
from app.config import settings, CSV_DIR

def apply_pca(features_df):
    pca = PCA(n_components=settings.PCA_COMPONENTS, random_state=settings.RANDOM_STATE)
    pca_result = pca.fit_transform(features_df)
    
    cols = [f"PC{i+1}" for i in range(pca_result.shape[1])]
    pca_df = pd.DataFrame(pca_result, index=features_df.index, columns=cols)
    
    pca_df.to_csv(CSV_DIR / "pca_features.csv")
    
    explained_var = {
        "explained_variance_ratio": pca.explained_variance_ratio_.tolist(),
        "cumulative_variance": pca.explained_variance_ratio_.cumsum().tolist()
    }
    
    return pca_df, explained_var
