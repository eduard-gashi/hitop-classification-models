from typing import Dict, Optional
import pandas as pd
from scipy.stats import ttest_ind
import numpy as np
from statsmodels.stats.outliers_influence import variance_inflation_factor
from statsmodels.tools.tools import add_constant


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


def calculate_statistic_significance(
    df: pd.DataFrame, 
    diagnosis_code: str
) -> pd.DataFrame:
    question_cols = [col for col in df.columns if not "Diagnose" in str(col[0])]
    diagnose_flag_col = (diagnosis_code, "")

    results = []
    for col in question_cols:
        values_true = df[df[diagnose_flag_col]==True][col].dropna()
        values_false = df[df[diagnose_flag_col]==False][col].dropna()
        
        values_true = values_true.astype(float)
        values_false = values_false.astype(float)

        if len(values_true) >= 2 and len(values_false) >= 2:
            stat, p_value = ttest_ind(values_true, values_false, equal_var=False)
            results.append({
                'question': col,
                'mean_true': values_true.mean(),
                'mean_false': values_false.mean(),
                'p_value': p_value,
            })
        else:
            results.append({
                'question': col,
                'mean_true': values_true.mean() if len(values_true) else None,
                'mean_false': values_false.mean() if len(values_false) else None,
                'p_value': None,
            })

    results_df = pd.DataFrame(results)

    return results_df


def calculate_vif_per_questionnaire(
    frageboegen: Dict[str, pd.DataFrame], 
    threshold: float = 5.0,
    head: int = 10
) -> Dict[str, pd.DataFrame]:
    """
    Hauptfunktion: Iteriert über Fragebögen und koordiniert die VIF-Berechnung.
    """
    print("\n" + "=" * 60)
    print("🔎 VIF ANALYSE (MULTIKOLLINEARITÄT)")
    print("=" * 60)

    results = {}

    for name, df in frageboegen.items():
        # 1. Vorverarbeitung
        df_clean = _preprocess_data(df)
        if df_clean is None:
            continue
        
        n_total_cols = df_clean.shape[1]

        # 2. Berechnung
        vif_df = _compute_vif_metrics(df_clean)
        if vif_df is None:
            print(f"⚠️ Fehler bei der Berechnung für {name}")
            continue

        # 3. Filterung & Ausgabe
        high_vif = vif_df[vif_df["VIF"] > threshold]
        
        if not high_vif.empty:
            _print_vif_results(name, n_total_cols, high_vif, threshold, head)
            results[name] = high_vif

    print("\n" + "=" * 60)
    return results


# --- HILFSFUNKTIONEN (Private Helpers) ---

def _preprocess_data(df: pd.DataFrame) -> Optional[pd.DataFrame]:
    """
    Bereinigt den DataFrame: Nur Zahlen, keine NaNs, saubere Spaltennamen.
    Gibt None zurück, wenn die Daten unzureichend sind.
    """
    # Nur Numerik & DropNA
    df_numeric = df.select_dtypes(include=[np.number]).dropna()

    if df_numeric.empty or df_numeric.shape[1] < 2:
        return None

    # Spaltennamen bereinigen
    clean_names = [_clean_column_name(col) for col in df_numeric.columns]
    df_numeric.columns = clean_names
    
    return df_numeric


def _clean_column_name(col: any) -> str:
    """
    Extrahiert einen kurzen, lesbaren Namen aus Tupeln oder langen Strings.
    """
    if isinstance(col, tuple):
        # Nimm das letzte Element des Tupels (oft der Code)
        name = str(col[-1])
    else:
        name = str(col)
    
    # Kürzen, falls extrem lang
    if len(name) > 20:
        return name[:17] + "..."
    return name


def _compute_vif_metrics(df: pd.DataFrame) -> Optional[pd.DataFrame]:
    """
    Führt die eigentliche mathematische VIF-Berechnung durch.
    """
    try:
        # Konstante hinzufügen (nötig für statsmodels)
        X = add_constant(df)
        
        # VIF für jede Spalte berechnen
        vif_data = pd.DataFrame()
        vif_data["Variable"] = X.columns
        vif_data["VIF"] = [variance_inflation_factor(X.values, i) 
                           for i in range(X.shape[1])]
        
        # 'const'-Zeile entfernen und sortieren
        return vif_data[vif_data["Variable"] != "const"].sort_values("VIF", ascending=False)
    
    except Exception:
        # Fängt Fehler ab (z.B. singuläre Matrix bei perfekter Korrelation)
        return None


def _print_vif_results(name: str, n_total: int, df_vif: pd.DataFrame, threshold: float, head: int):
    """
    Kümmert sich ausschließlich um die schöne Formatierung der Ausgabe.
    """
    n_critical = len(df_vif)
    
    print(f"\n➡️  Fragebogen: {name} (Gesamt: {n_total} Items)")
    print(f"   ⚠️  {n_critical} von {n_total} Items mit VIF > {threshold}")
    print(f"   {'Variable':<20} | {'VIF':<10}")
    print(f"   {'-'*32}")
    
    # Top X anzeigen
    for _, row in df_vif.head(head).iterrows():
        print(f"   {row['Variable']:<20} | {row['VIF']:<10.2f}")
    
    # Hinweis auf weitere Items
    if n_critical > head:
        print(f"   ... (+ {n_critical - head} weitere)")