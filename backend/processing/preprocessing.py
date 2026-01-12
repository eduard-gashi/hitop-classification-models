from typing import Dict
import pandas as pd


def extract_columns_from_questionnaire(
    pre_frageboegen: Dict[str, pd.DataFrame], rw: bool, questions: bool, diagnosis: bool
) -> Dict[str, pd.DataFrame]:
    """Extract only specific columns from the questionnaires."""
    sliced_questionnaires = {}

    for name, df in pre_frageboegen.items():
        all_cols = list(df.columns)

        rw_cols = [col for col in all_cols if "rw" in str(col).lower()]
        diagnosis_cols = [col for col in all_cols if str(col[0]).startswith("Diagnose")]
        question_cols = [col for col in all_cols if col not in rw_cols + diagnosis_cols]
        
        cols_to_keep = []
        if rw:
            cols_to_keep.extend(rw_cols)
        if questions:
            cols_to_keep.extend(question_cols)
        if diagnosis:
            cols_to_keep.extend(diagnosis_cols)

        sliced_questionnaires[name] = df[cols_to_keep].copy()

    return sliced_questionnaires


def add_diagnosis_presence_column(
    questionnaires_dict: Dict[str, pd.DataFrame],
    questionnaire_name: str,
    diagnosis_code: str,
) -> pd.DataFrame:
    """Adds a column to the DataFrame indicating whether a diagnosis is given for a patience or not."""
    df = questionnaires_dict[questionnaire_name]
    
    # Create a column indicating the presence of the diagnosis code for a participant
    df[diagnosis_code] = df.apply(
        lambda row: True if diagnosis_code in row.values else False, axis=1
    )

    return df
