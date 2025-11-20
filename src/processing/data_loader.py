import pandas as pd
from pathlib import Path
from src.config import (
    ORIGINAL_PRE_DATASET,
    ORIGINAL_POST_DATASET,
    ORIGINAL_TEST_VARIABLES,
    STANDARDIZED_PRE_DATASET,
    STANDARDIZED_POST_DATASET,
    SAMPLED_PRE_DATASET,
    SAMPLED_POST_DATASET,
)

def safe_read_excel(path, **kwargs):
    if Path(path).exists():
        return pd.read_excel(path, **kwargs)
    else: 
        print(f"Error: Datei nicht gefunden - {path}")
        return None

def load_data(data_type="processed"):
    """
    Loads therapy rating datasets.

    Parameters:
    -----------
    data_type : str, default='processed'
        Type of data to load. Options:
        - 'raw' or 'original': Loads original datasets
        - 'processed' or 'sampled': Loads sampled/processed datasets

    Returns:
    --------
    tuple of pd.DataFrame
        (df_test_vars, df_pre, df_post) - Test variables dataframe, pre and post therapy rating dataframes
    """
    if data_type in ["raw", "original"]:
        df_pre = safe_read_excel(ORIGINAL_PRE_DATASET)
        df_post = safe_read_excel(ORIGINAL_POST_DATASET)
    elif data_type == "standardized":
        df_pre = safe_read_excel(STANDARDIZED_PRE_DATASET)
        df_post = safe_read_excel(STANDARDIZED_POST_DATASET)
    elif data_type in ["processed", "sampled"]:
        df_pre = safe_read_excel(SAMPLED_PRE_DATASET)
        df_post = safe_read_excel(SAMPLED_POST_DATASET)
    else:
        raise ValueError(
            f"Invalid data_type: {data_type}. Use 'raw', 'original', 'processed', or 'sampled'."
        )

    df_test_vars = safe_read_excel(ORIGINAL_TEST_VARIABLES)

    return df_test_vars, df_pre, df_post