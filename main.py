import pandas as pd
from pathlib import Path
from typing import List, Dict


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


def split_df_by_questionnaire(
    therapy_ratings_df: pd.DataFrame, 
    metadata_df: pd.DataFrame
) -> Dict[str, pd.DataFrame]:
    """
    Split a DataFrame of therapy ratings into separate DataFrames by questionnaire ('Test').

    Parameters
    ----------
    therapy_ratings_df : pd.DataFrame
        The main DataFrame containing the therapy ratings.
    metadata_df : pd.DataFrame
        Metadata DataFrame containing the 'Test' column which represents the name of the distinct questionnaires.

    Returns
    -------
    Dict[str, pd.DataFrame]
        Dictionary where each key is a questionnaire name ('Test'), and each value is the DataFrame for that questionnaire.

    Example
    -------
    >>> questionnaires = split_df_by_questionnaire(ratings_df, meta_df)
    >>> for questionnaire, questionnaire_df in questionnaires.items():
    ...     print(f"{name}: shape={df.shape}")
    """
    # Extract the code (e.g. 'waiai301', 'phqai014', etc.) from the MultiIndex (second level)
    codes = [col[1] for col in therapy_ratings_df.columns]

    # Map each variable code to its questionnaire ('Test') as given in the metadata
    code_to_test = metadata_df.set_index('Variablenname')['Test'].to_dict()

    # Map test assignments to each column in the DataFrame
    column_tests = [code_to_test.get(code, "Unbekannt") for code in codes]

    # Get the unique set of questionnaire names
    unique_tests = set(column_tests)

    # Build a dictionary: {questionnaire_name: DataFrame of that questionnaire}
    questionnaires_dict = {}
    for test in unique_tests:
        relevant_columns = [col for col, t in zip(therapy_ratings_df.columns, column_tests) if t == test]
        questionnaires_dict[test] = therapy_ratings_df.loc[:, relevant_columns].copy()

    return questionnaires_dict


def count_answers_per_fragebogen(frageboegen: List[pd.DataFrame]) -> List[Dict[str, int]]:
    #TODO: Implement function to count answers per 'Fragebogen' (Maxim)
    pass


def plot_results(answers_count: List[Dict[str, int]]):
    #TODO: Implement visualiation of the results (David)
    pass 


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
    
    df_pre_therapy_ratings = split_df_by_fragebogen(df_pre_therapy_ratings)
    

if __name__ == "__main__":
    main()
