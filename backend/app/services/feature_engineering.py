import pandas as pd
import numpy as np
from scipy import stats
from app.config import CSV_DIR

def engineer_features(m_pivot, t_pivot, relation_map):
    V = m_pivot.values
    
    features = pd.DataFrame(index=m_pivot.index)
    
    # A. Basic
    features["mean"] = np.mean(V, axis=1)
    features["median"] = np.median(V, axis=1)
    features["min"] = np.min(V, axis=1)
    features["max"] = np.max(V, axis=1)
    features["std"] = np.std(V, axis=1)
    features["var"] = np.var(V, axis=1)
    features["range"] = np.ptp(V, axis=1)
    features["iqr"] = stats.iqr(V, axis=1)
    features["cv"] = features["std"] / (features["mean"] + 1e-9)
    features["skew"] = stats.skew(V, axis=1)
    features["kurtosis"] = stats.kurtosis(V, axis=1)

    # B. Temporal
    if V.shape[1] > 1:
        diff1 = np.diff(V, axis=1)
        features["diff1_mean"] = np.mean(diff1, axis=1)
        features["diff1_std"] = np.std(diff1, axis=1)
        features["abs_diff_mean"] = np.mean(np.abs(diff1), axis=1)

        # Autocorrelation lag 1
        v0 = V[:, :-1]; v1 = V[:, 1:]
        m0 = v0.mean(axis=1, keepdims=True)
        m1 = v1.mean(axis=1, keepdims=True)
        num = np.sum((v0 - m0) * (v1 - m1), axis=1)
        den = np.sqrt(np.sum((v0 - m0)**2, axis=1) * np.sum((v1 - m1)**2, axis=1))
        features["lag1_auto"] = num / (den + 1e-9)
    else:
        features["diff1_mean"] = 0
        features["diff1_std"] = 0
        features["abs_diff_mean"] = 0
        features["lag1_auto"] = 0

    # Autocorrelation lag 2
    if V.shape[1] > 2:
        v0_2 = V[:, :-2]; v2 = V[:, 2:]
        m0_2 = v0_2.mean(axis=1, keepdims=True)
        m2 = v2.mean(axis=1, keepdims=True)
        num_2 = np.sum((v0_2 - m0_2) * (v2 - m2), axis=1)
        den_2 = np.sqrt(np.sum((v0_2 - m0_2)**2, axis=1) * np.sum((v2 - m2)**2, axis=1))
        features["lag2_auto"] = num_2 / (den_2 + 1e-9)
    else:
        features["lag2_auto"] = 0

    # C. Transformer-Relative
    relation_dict = dict(zip(relation_map['consumer_id'], relation_map['transformer_id']))
    T_V = np.zeros_like(V)
    t_pivot_idx = set(t_pivot.index)
    
    for i, c_id in enumerate(m_pivot.index):
        t_id = relation_dict.get(c_id)
        if t_id in t_pivot_idx:
            T_V[i] = t_pivot.loc[t_id].values

    diff_t = V - T_V
    features["t_diff_mean"] = np.mean(diff_t, axis=1)
    features["t_diff_std"] = np.std(diff_t, axis=1)
    features["t_mae"] = np.mean(np.abs(diff_t), axis=1)
    
    m_V = V.mean(axis=1, keepdims=True)
    m_T = T_V.mean(axis=1, keepdims=True)
    num_c = np.sum((V - m_V) * (T_V - m_T), axis=1)
    den_c = np.sqrt(np.sum((V - m_V)**2, axis=1) * np.sum((T_V - m_T)**2, axis=1))
    features["t_corr"] = num_c / (den_c + 1e-9)

    features = features.fillna(0)
    
    # Standardize features globally
    df_feat = (features - features.mean()) / (features.std() + 1e-9)
    df_feat.to_csv(CSV_DIR / "engineered_features.csv")
    
    return df_feat
