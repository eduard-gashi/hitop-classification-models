import pandas as pd
from pathlib import Path


def load_data():
    current_dir = Path(__file__).parent
    dataset_dir = current_dir / 'Original Dataset'
    
    df_test_variables = pd.read_excel(dataset_dir / 'Test-Variablen Software ab 2014.xlsx')
    df_pre_therapy_ratings = pd.read_excel(dataset_dir / 'Reha BG 2014-2022 prä Daten+Ther.ratings_anonym(1).xlsx')
    df_post_therapy_ratings = pd.read_excel(dataset_dir / 'Reha BG 2014-2022 post Daten_anonym(1).xlsx')

    return df_test_variables, df_pre_therapy_ratings, df_post_therapy_ratings


def attach_metadata_as_multiindex(therapy_ratings_df, metadata_df, metadata_column='Variablenlabel'):
    # Delete duplicates in metadata and therapy_ratings DataFrames
    if metadata_df['Variablenname'].duplicated().any():
        metadata_df = metadata_df.drop_duplicates(subset=['Variablenname'], keep='first')
        
    if therapy_ratings_df.columns.duplicated().any():
        therapy_ratings_df = therapy_ratings_df.loc[:, ~therapy_ratings_df.columns.duplicated(keep='first')]
    
    # Lookupup-Table: Mapping from Codes to desired metadata 
    metadata_lookup = metadata_df.set_index('Variablenname')[metadata_column]
    sorted_metadata = metadata_lookup.reindex(therapy_ratings_df.columns)
        
    # Create MultiIndex from metadata
    multi_index = pd.MultiIndex.from_arrays(
        [
            sorted_metadata.fillna(f'Unbekannt: {metadata_column}'),  # Layer 1: Metadata labels
            sorted_metadata.index # Layer 2: Original variable codes
        ],
        names=[metadata_column, 'Code']
    )
    
    therapy_ratings_df.columns = multi_index
    
    return therapy_ratings_df


def main():
    df_metadata, df_pre_therapy_ratings, df_post_therapy_ratings = load_data()
        
        
    df_pre_therapy_ratings = attach_metadata_as_multiindex(
        therapy_ratings_df=df_pre_therapy_ratings.copy(),
        metadata_df=df_metadata,
        metadata_column='Variablenlabel' # Possible columns [Frage, Variablenlabel, Test, Skala, Anmerkung]
    )
    
    df_post_therapy_ratings = attach_metadata_as_multiindex(
        therapy_ratings_df=df_post_therapy_ratings.copy(),
        metadata_df=df_metadata,
        metadata_column='Variablenlabel' # Possible columns [Frage, Variablenlabel, Test, Skala, Anmerkung]
    )
    print("Pre-Therapy Ratings with MultiIndex:")
    

if __name__ == "__main__":
    main()
