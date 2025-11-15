import pandas as pd
import os 

base_path = os.getcwd()

original_dataset_path = os.path.join(base_path, "data", "raw")

pre_dataset_path = os.path.join(original_dataset_path, "pre_dataset_standardized.xlsx")
post_dataset_path = os.path.join(original_dataset_path, "post_dataset.xlsx")

sampled_dataset_path = os.path.abspath(os.path.join(original_dataset_path, "..", "processed\\"))

# Einlesen der Original-Datensätze
df_pre = pd.read_excel(pre_dataset_path)
df_post = pd.read_excel(post_dataset_path)


pre_sampled = df_pre.sample(n=1000, random_state=42)
ids = pre_sampled["Code"]

# Damit die selben Patienten im Post-Datensatz sind
post_sampled = df_post[df_post["Code"].isin(ids)]

# Exportieren der gesampelten Datensätze
pre_sampled.to_excel(os.path.join(sampled_dataset_path, "pre_dataset.xlsx"), index=False)
post_sampled.to_excel(os.path.join(sampled_dataset_path, "post_dataset.xlsx"), index=False)
