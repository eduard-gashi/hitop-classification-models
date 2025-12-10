import pandas as pd
from typing import Dict

def attach_metadata_as_multiindex(
    therapy_ratings_df, metadata_df, metadata_column="Variablenlabel"
):
    """Fügt Metadaten als MultiIndex zu den Spalten hinzu."""
    if metadata_df["Variablenname"].duplicated().any():
        metadata_df = metadata_df.drop_duplicates(
            subset=["Variablenname"], keep="first"
        )

    if therapy_ratings_df.columns.duplicated().any():
        therapy_ratings_df = therapy_ratings_df.loc[
            :, ~therapy_ratings_df.columns.duplicated(keep="first")
        ]

    metadata_lookup = metadata_df.set_index("Variablenname")[metadata_column]
    sorted_metadata = metadata_lookup.reindex(therapy_ratings_df.columns)

    multi_index = pd.MultiIndex.from_arrays(
        [
            sorted_metadata.fillna(f"Unbekannt: {metadata_column}"),
            sorted_metadata.index,
        ],
        names=[metadata_column, "Code"],
    )

    therapy_ratings_df.columns = multi_index

    return therapy_ratings_df


def split_df_by_questionnaire(
    therapy_ratings_df: pd.DataFrame,
    metadata_df: pd.DataFrame,
    include_diagnosis_cols: bool = False,
) -> Dict[str, pd.DataFrame]:
    """Split a DataFrame of therapy ratings into separate DataFrames by questionnaire ('Test')."""
    codes = [col[1] for col in therapy_ratings_df.columns]
    code_to_test = metadata_df.set_index("Variablenname")["Test"].to_dict()
    column_tests = [code_to_test.get(code, "Unbekannt") for code in codes]
    unique_tests = set(column_tests)

    questionnaires_dict = {}
    for test in unique_tests:
        if test == "Unbekannt":
            continue
        relevant_columns = [
            col for col, t in zip(therapy_ratings_df.columns, column_tests) if t == test
        ]
        if include_diagnosis_cols:
            diagnosis_columns = [
                col
                for col in therapy_ratings_df.columns
                if str(col[0]).startswith("Diagnose")
            ]
            relevant_columns.extend(diagnosis_columns)
        questionnaires_dict[test] = therapy_ratings_df.loc[:, relevant_columns].copy()

    return questionnaires_dict


