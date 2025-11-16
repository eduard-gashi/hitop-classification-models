from src.processing.data_loader import load_data
from config import(
    SAMPLED_PRE_DATASET,
    SAMPLED_POST_DATASET,
)



def sample_data(sample_size = 1000, dataset = "standardized", random_state = 42):
    _, df_pre, df_post = load_data(data_type=dataset)

    pre_exists = df_pre is not None and not df_pre.empty
    post_exists = df_post is not None and not df_post.empty

    if pre_exists and post_exists:

        pre_sampled = df_pre.sample(n = sample_size, random_state = random_state)
        ids = pre_sampled["Code"]
        post_sampled = df_post[df_post["Code"].isin(ids)]
        
        pre_sampled.to_excel(SAMPLED_PRE_DATASET, index = False)
        print(f"Sampled {sample_size} samples from {dataset} pre-dataset. Saved at {SAMPLED_PRE_DATASET}")

        post_sampled.to_excel(SAMPLED_POST_DATASET, index = False)
        print(f"Filtered post-dataset to matching IDs. Saved at {SAMPLED_POST_DATASET}")
       
    elif pre_exists:
        pre_sampled = df_pre.sample(n = sample_size, random_state = random_state)
        pre_sampled.to_excel(SAMPLED_PRE_DATASET, index=False)
        print(f"Sampled {sample_size} samples from {dataset} pre-dataset. Saved dataset at {SAMPLED_PRE_DATASET}")

    elif post_exists:
        post_sampled = df_post.sample(n = sample_size, random_state = random_state)
        post_sampled.to_excel(SAMPLED_POST_DATASET, index=False)
        print(f"Sampled {sample_size} samples from {dataset} post-dataset. Saved dataset at {SAMPLED_POST_DATASET}")

    else:
        print("Fehler: Keiner der beiden Datensätze ist vorhanden!")
    

if __name__ == "__main__":
    sample_data()