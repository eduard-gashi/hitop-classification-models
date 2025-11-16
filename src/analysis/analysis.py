from typing import Dict
import pandas as pd


def count_answers_per_fragebogen(
    frageboegen: Dict[str, pd.DataFrame],
) -> Dict[str, int]:
    """Count the total number of non-NA answers per questionnaire."""
    result = {}
    for name, df in frageboegen.items():
        result[name] = df.count().sum()
    return result


def calculate_statistics(
    normalized_df: pd.DataFrame, original_df: pd.DataFrame
) -> Dict:
    """
    Berechnet statistische Kennwerte für normalisierte und originale Daten.

    Parameters
    ----------
    normalized_df : pd.DataFrame
        Z-Score normalisierte Daten
    original_df : pd.DataFrame
        Original-Daten

    Returns
    -------
    Dict
        Dictionary mit statistischen Kennwerten
    """
    stats = {
        "normalized": {
            "mean": normalized_df.mean(),
            "std": normalized_df.std(),
            "median": normalized_df.median(),
            "min": normalized_df.min(),
            "max": normalized_df.max(),
            "q25": normalized_df.quantile(0.25),
            "q75": normalized_df.quantile(0.75),
            "skewness": normalized_df.skew(),
            "kurtosis": normalized_df.kurtosis(),
        },
        "original": {
            "mean": original_df.mean(),
            "std": original_df.std(),
            "median": original_df.median(),
            "min": original_df.min(),
            "max": original_df.max(),
            "q25": original_df.quantile(0.25),
            "q75": original_df.quantile(0.75),
            "skewness": original_df.skew(),
            "kurtosis": original_df.kurtosis(),
        },
    }
    return stats


def print_statistics(stats: Dict, fragebogen_name: str):
    """
    Gibt statistische Kennwerte formatiert aus.

    Parameters
    ----------
    stats : Dict
        Dictionary mit statistischen Kennwerten
    fragebogen_name : str
        Name des Fragebogens
    """
    print("\n" + "=" * 80)
    print(f"STATISTISCHE AUSWERTUNG: {fragebogen_name}")
    print("=" * 80)

    # Normalisierte Daten
    print("\n📊 NORMALISIERTE DATEN (Z-Score):")
    print("-" * 80)
    norm_stats = stats["normalized"]

    print(
        f"\n{'Frage':<15} {'Mittel':<10} {'Std':<10} {'Median':<10} {'Min':<10} {'Max':<10}"
    )
    print("-" * 80)
    for col in norm_stats["mean"].index:
        print(
            f"{col:<15} {norm_stats['mean'][col]:>9.3f} {norm_stats['std'][col]:>9.3f} "
            f"{norm_stats['median'][col]:>9.3f} {norm_stats['min'][col]:>9.3f} {norm_stats['max'][col]:>9.3f}"
        )

    print(f"\n{'Frage':<15} {'Q25':<10} {'Q75':<10} {'Schiefe':<12} {'Kurtosis':<10}")
    print("-" * 80)
    for col in norm_stats["mean"].index:
        print(
            f"{col:<15} {norm_stats['q25'][col]:>9.3f} {norm_stats['q75'][col]:>9.3f} "
            f"{norm_stats['skewness'][col]:>11.3f} {norm_stats['kurtosis'][col]:>9.3f}"
        )

    # Original-Daten
    print("\n\n📈 ORIGINAL-DATEN:")
    print("-" * 80)
    orig_stats = stats["original"]

    print(
        f"\n{'Frage':<15} {'Mittel':<10} {'Std':<10} {'Median':<10} {'Min':<10} {'Max':<10}"
    )
    print("-" * 80)
    for col in orig_stats["mean"].index:
        print(
            f"{col:<15} {orig_stats['mean'][col]:>9.3f} {orig_stats['std'][col]:>9.3f} "
            f"{orig_stats['median'][col]:>9.3f} {orig_stats['min'][col]:>9.3f} {orig_stats['max'][col]:>9.3f}"
        )

    print(f"\n{'Frage':<15} {'Q25':<10} {'Q75':<10} {'Schiefe':<12} {'Kurtosis':<10}")
    print("-" * 80)
    for col in orig_stats["mean"].index:
        print(
            f"{col:<15} {orig_stats['q25'][col]:>9.3f} {orig_stats['q75'][col]:>9.3f} "
            f"{orig_stats['skewness'][col]:>11.3f} {orig_stats['kurtosis'][col]:>9.3f}"
        )

    print("\n" + "=" * 80)


def get_rw_columns(
    pre_frageboegen: Dict[str, pd.DataFrame], keep_diagnosis_cols: bool
) -> Dict[str, pd.DataFrame]:
    """Extract only the columns with the RW-Codes out of the dataframe."""
    pre_frageboegen_rw = {}

    for name, df in pre_frageboegen.items():
        rw_cols = []
        if keep_diagnosis_cols:
            rw_cols += [col for col in df.columns if str(col[0]).startswith("Diagnose")]
        rw_cols += [col for col in df.columns if "rw" in str(col).lower()]
        pre_frageboegen_rw[name] = df[rw_cols].copy()

    return pre_frageboegen_rw


def get_questionnaire_means_by_diagnosis(
    questionnaires_dict: Dict[str, pd.DataFrame],
    questionnaire_name: str,
    diagnosis_code: str,
) -> pd.DataFrame:
    """Extracts mean for every answer of a questionnaire based on whether a diagnosis is given or not."""
    df = questionnaires_dict[questionnaire_name]

    # Create a column indicating the presence of the diagnosis code for a participant
    df[diagnosis_code] = df.apply(
        lambda row: True if diagnosis_code in row.values else False, axis=1
    )

    question_cols = [col for col in df.columns if not "Diagnose" in str(col[0])]

    mean_false = []
    mean_true = []

    for col in question_cols:
        val_false = df[df[(diagnosis_code, "")] == False][col].mean()
        val_true = df[df[(diagnosis_code, "")] == True][col].mean()
        mean_false.append(val_false)
        mean_true.append(val_true)

    result_df = pd.DataFrame(
        columns=question_cols,
        data=[mean_false, mean_true],
        index=[f"{diagnosis_code}=False", f"{diagnosis_code}=True"],
    )

    return result_df