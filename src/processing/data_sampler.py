import pandas as pd
from src.processing.data_loader import load_data
from config import(
    SAMPLED_PRE_DATASET,
    SAMPLED_POST_DATASET,
)

df_test_vars, df_pre, df_post = load_data()

pre_sampled = df_pre.sample(n=1000, random_state=42)
ids = pre_sampled["Code"]

# Damit die selben Patienten im Post-Datensatz sind
post_sampled = df_post[df_post["Code"].isin(ids)]

# Exportieren der gesampelten Datensätze
pre_sampled.to_excel(SAMPLED_PRE_DATASET, index=False)
post_sampled.to_excel(SAMPLED_POST_DATASET, index=False)
