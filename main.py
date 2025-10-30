import pandas as pd
from pathlib import Path


def load_data():
    current_dir = Path(__file__).parent
    dataset_dir = current_dir / 'Original Dataset'
    
    df_test_variables = pd.read_excel(dataset_dir / 'Test-Variablen Software ab 2014.xlsx')
    df_pre_therapy_ratings = pd.read_excel(dataset_dir / 'Reha BG 2014-2022 prä Daten+Ther.ratings_anonym(1).xlsx')
    df_post_therapy_ratings = pd.read_excel(dataset_dir / 'Reha BG 2014-2022 post Daten_anonym(1).xlsx')

    return df_test_variables, df_pre_therapy_ratings, df_post_therapy_ratings


def main():
    df_test_variables, df_pre_therapy_ratings, df_post_therapy_ratings = load_data()
    print("Test Variables DataFrame:")
    print(df_test_variables.head())
    
    print("\nPre Therapy Ratings DataFrame:")
    print(df_pre_therapy_ratings.head())
    
    print("\nPost Therapy Ratings DataFrame:")
    print(df_post_therapy_ratings.head())


if __name__ == "__main__":
    main()
