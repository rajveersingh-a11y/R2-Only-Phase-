import pandas as pd
import numpy as np
from app.config import CSV_DIR

def preprocess_data(meters_df, trans_df, gt_df):
    # Find relevant columns flexibly
    def find_col(df, keywords):
        for col in df.columns:
            if any(k in col for k in keywords):
                return col
        return None

    # GroundTruth Columns
    gt_cm_col = find_col(gt_df, ["consumer", "meter"])
    gt_tr_col = find_col(gt_df, ["transformer", "dt"])
    
    # Create mapping
    relation_map = gt_df[[gt_cm_col, gt_tr_col]].dropna().copy()
    relation_map.columns = ["consumer_id", "transformer_id"]
    relation_map['consumer_id'] = relation_map['consumer_id'].astype(str)
    relation_map['transformer_id'] = relation_map['transformer_id'].astype(str)
    
    # Restructure Meters
    m_id_col = find_col(meters_df, ["id", "meter", "consumer"])
    m_time_col = find_col(meters_df, ["time", "date"])
    m_volt_col = find_col(meters_df, ["volt", "v"])
    
    m_clean = meters_df[[m_id_col, m_time_col, m_volt_col]].dropna(subset=[m_id_col]).copy()
    m_clean.columns = ["consumer_id", "timestamp", "voltage"]
    m_clean['consumer_id'] = m_clean['consumer_id'].astype(str)
    
    # Restructure Transformers
    t_id_col = find_col(trans_df, ["id", "transformer", "dt"])
    t_time_col = find_col(trans_df, ["time", "date"])
    t_volt_col = find_col(trans_df, ["volt", "v"])
    
    t_clean = trans_df[[t_id_col, t_time_col, t_volt_col]].dropna(subset=[t_id_col]).copy()
    t_clean.columns = ["transformer_id", "timestamp", "voltage"]
    t_clean['transformer_id'] = t_clean['transformer_id'].astype(str)
    
    # Pivot time series
    m_pivot = m_clean.pivot_table(index="consumer_id", columns="timestamp", values="voltage", aggfunc="mean")
    t_pivot = t_clean.pivot_table(index="transformer_id", columns="timestamp", values="voltage", aggfunc="mean")
    
    # Align timestamps
    common_times = m_pivot.columns.intersection(t_pivot.columns)
    m_pivot = m_pivot[common_times]
    t_pivot = t_pivot[common_times]
    
    # Impute missing
    m_pivot = m_pivot.interpolate(axis=1, method='linear').fillna(method='bfill', axis=1).fillna(method='ffill', axis=1)
    t_pivot = t_pivot.interpolate(axis=1, method='linear').fillna(method='bfill', axis=1).fillna(method='ffill', axis=1)
    
    m_pivot.to_csv(CSV_DIR / "clean_consumer_voltage.csv")
    t_pivot.to_csv(CSV_DIR / "clean_transformer_voltage.csv")
    
    return m_pivot, t_pivot, relation_map
