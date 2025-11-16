import pandas as pd
from config import (
    ORIGINAL_PRE_DATASET,
    ORIGINAL_POST_DATASET,
    ORIGINAL_TEST_VARIABLES,
    SAMPLED_PRE_DATASET,
    SAMPLED_POST_DATASET,
)


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
        df_pre = pd.read_excel(ORIGINAL_PRE_DATASET)
        df_post = pd.read_excel(ORIGINAL_POST_DATASET)
    elif data_type in ["processed", "sampled"]:
        df_pre = pd.read_excel(SAMPLED_PRE_DATASET)
        df_post = pd.read_excel(SAMPLED_POST_DATASET)
    else:
        raise ValueError(
            f"Invalid data_type: {data_type}. Use 'raw', 'original', 'processed', or 'sampled'."
        )

    df_test_vars = pd.read_excel(ORIGINAL_TEST_VARIABLES)

    return df_test_vars, df_pre, df_post

load_data()