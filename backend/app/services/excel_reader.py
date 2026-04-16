import pandas as pd
import numpy as np
from app.utils import get_clean_col_names

def load_data(file_path):
    xls = pd.ExcelFile(file_path)
    
    # Needs flexible name matching
    sheet_names = [s.lower() for s in xls.sheet_names]
    
    meters_sheet = next((s for s in xls.sheet_names if "meter" in s.lower()), None)
    trans_sheet = next((s for s in xls.sheet_names if "transformer_voltage" in s.lower().replace(" ", "_")), None)
    gt_sheet = next((s for s in xls.sheet_names if "groundtruth" in s.lower().replace(" ", "")), None)
    
    if not all([meters_sheet, trans_sheet, gt_sheet]):
        raise ValueError("Could not find all required sheets (Meters, Transformer_Voltages, GroundTruth)")
        
    meters_df = pd.read_excel(file_path, sheet_name=meters_sheet)
    trans_df = pd.read_excel(file_path, sheet_name=trans_sheet)
    gt_df = pd.read_excel(file_path, sheet_name=gt_sheet)
    
    meters_df.columns = get_clean_col_names(meters_df.columns)
    trans_df.columns = get_clean_col_names(trans_df.columns)
    gt_df.columns = get_clean_col_names(gt_df.columns)
    
    return meters_df, trans_df, gt_df
