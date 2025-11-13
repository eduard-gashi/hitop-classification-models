from pathlib import Path

# Base directory
BASE_DIR = Path(__file__).parent

# Data paths
DATA_DIR = BASE_DIR / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
PROCESSED_DATA_DIR = DATA_DIR / "processed"

# Original datasets
ORIGINAL_DATASET_DIR = RAW_DATA_DIR
ORIGINAL_PRE_DATASET = ORIGINAL_DATASET_DIR / "pre_dataset.xlsx"
ORIGINAL_POST_DATASET= ORIGINAL_DATASET_DIR / "post_dataset.xlsx"
ORIGINAL_TEST_VARIABLES = ORIGINAL_DATASET_DIR / "test_variables.xlsx"

# Sampled Dataset
SAMPLED_DATASET_DIR = PROCESSED_DATA_DIR
SAMPLED_PRE_DATASET = SAMPLED_DATASET_DIR / "pre_dataset.xlsx"
SAMPLED_POST_DATASET = SAMPLED_DATASET_DIR / "post_dataset.xlsx"
SAMPLED_PRE_DATASET_CSV = SAMPLED_DATASET_DIR / "pre_dataset.csv"

# Output paths
OUTPUT_DIR = BASE_DIR / "outputs"
PLOTS_DIR = OUTPUT_DIR / "plots"
RESULTS_DIR = OUTPUT_DIR / "results"

#TODO: other constants