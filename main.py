import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from pathlib import Path
from typing import Dict
from sklearn.preprocessing import StandardScaler
from config import (
    ORIGINAL_PRE_DATASET,
    ORIGINAL_POST_DATASET,
    ORIGINAL_TEST_VARIABLES,
    SAMPLED_PRE_DATASET,
    SAMPLED_PRE_DATASET_CSV,
    SAMPLED_POST_DATASET,
    PLOTS_DIR,
    RESULTS_DIR,
)


def load_data(data_type="processed"):
    """
    Loads therapy rating datasets.

    Parameters:
    -----------
    data_type : str, default='processed'
        Type of data to load. Options:
        - 'raw' or 'original': Loads original datasets
        - 'processed' or 'sampled': Loads sampled/processed datasets

    Returns:
    --------
    tuple of pd.DataFrame
        (df_test_vars, df_pre, df_post) - Test variables dataframe, pre and post therapy rating dataframes
    """
    if data_type in ["raw", "original"]:
        df_pre = pd.read_excel(ORIGINAL_PRE_DATASET)
        df_post = pd.read_excel(ORIGINAL_POST_DATASET)
    elif data_type in ["processed", "sampled"]:
        df_pre = pd.read_csv(SAMPLED_PRE_DATASET_CSV)
        df_post = pd.read_excel(SAMPLED_POST_DATASET)
    else:
        raise ValueError(
            f"Invalid data_type: {data_type}. Use 'raw', 'original', 'processed', or 'sampled'."
        )

    df_test_vars = pd.read_excel(ORIGINAL_TEST_VARIABLES)

    return df_test_vars, df_pre, df_post


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


def visualize_specific_fragebogen(
    frageboegen: Dict[str, pd.DataFrame], fragebogen_name: str, normalize=True
):
    """
    Visualisiert die Distributionen eines spezifischen Fragebogens.

    Parameters
    ----------
    frageboegen : Dict[str, pd.DataFrame]
        Dictionary mit allen Fragebogen-DataFrames
    fragebogen_name : str
        Name des Fragebogens, der visualisiert werden soll
    normalize : bool
        Ob die Daten für Boxplot normalisiert werden sollen (Standard: True)
    """
    if fragebogen_name not in frageboegen:
        print(f"Fehler: Fragebogen '{fragebogen_name}' nicht gefunden!")
        print(f"Verfügbare Fragebögen: {list(frageboegen.keys())}")
        return

    df = frageboegen[fragebogen_name]
    numeric_df = df.select_dtypes(include="number")

    if numeric_df.empty:
        print(f"{fragebogen_name}: Keine numerischen Daten vorhanden.")
        return

    print(f"\n=== Visualisierung: {fragebogen_name} ===")
    print(f"Shape: {numeric_df.shape}")
    print(f"Anzahl Spalten: {numeric_df.shape[1]}")
    print(f"Anzahl Zeilen: {numeric_df.shape[0]}\n")

    # Erstelle durchnummerierte Labels
    question_labels = [f"Frage-{i+1}" for i in range(numeric_df.shape[1])]

    # Umbenennung für alle Visualisierungen
    numeric_df_renamed = numeric_df.copy()
    numeric_df_renamed.columns = question_labels

    # 1. Histogramme für alle Spalten mit neuen Labels
    n_cols = numeric_df_renamed.shape[1]
    n_rows = int(np.ceil(n_cols / 4))

    fig, axes = plt.subplots(n_rows, 4, figsize=(16, 4 * n_rows))
    axes = axes.flatten() if n_cols > 1 else [axes]

    for i, col in enumerate(numeric_df_renamed.columns):
        axes[i].hist(
            numeric_df_renamed[col].dropna(),
            bins=20,
            edgecolor="black",
            color="steelblue",
        )
        axes[i].set_title(col, fontsize=10)
        axes[i].set_xlabel("Wert")
        axes[i].set_ylabel("Häufigkeit")
        axes[i].grid(alpha=0.3)

    # Leere Subplots ausblenden
    for i in range(n_cols, len(axes)):
        axes[i].set_visible(False)

    plt.suptitle(f"Histogramme – {fragebogen_name}", fontsize=16, fontweight="bold")
    plt.tight_layout()
    plt.show()

    # 2. Boxplots - Original vs. Normalisiert
    if normalize:
        # Z-Score Normalisierung (Standardisierung)
        scaler = StandardScaler()
        normalized_values = scaler.fit_transform(numeric_df.dropna())
        normalized_df = pd.DataFrame(normalized_values, columns=question_labels)

        # Plot beide: Original und Normalisiert
        fig, axes = plt.subplots(2, 1, figsize=(16, 12))

        # Original Boxplot
        numeric_df_renamed.plot(kind="box", ax=axes[0])
        axes[0].set_title(
            f"Boxplot (Original) – {fragebogen_name}", fontsize=14, fontweight="bold"
        )
        axes[0].set_ylabel("Original-Werte")
        axes[0].set_xlabel("Fragen")
        axes[0].grid(axis="y", alpha=0.3)
        axes[0].tick_params(axis="x", rotation=45)

        # Normalisierter Boxplot
        normalized_df.plot(kind="box", ax=axes[1])
        axes[1].set_title(
            f"Boxplot (Z-Score normalisiert) – {fragebogen_name}",
            fontsize=14,
            fontweight="bold",
        )
        axes[1].set_ylabel("Standardisierte Werte (Mittelwert=0, Std=1)")
        axes[1].set_xlabel("Fragen")
        axes[1].grid(axis="y", alpha=0.3)
        axes[1].tick_params(axis="x", rotation=45)

        plt.tight_layout()
        plt.show()

        # Berechne und gebe Statistiken aus
        stats = calculate_statistics(normalized_df, numeric_df_renamed)
        print_statistics(stats, fragebogen_name)

    else:
        # Nur Original-Boxplot
        plt.figure(figsize=(16, 6))
        numeric_df_renamed.plot(kind="box", ax=plt.gca())
        plt.title(f"Boxplot – {fragebogen_name}", fontsize=14, fontweight="bold")
        plt.xlabel("Fragen")
        plt.xticks(rotation=45, ha="right")
        plt.ylabel("Werte")
        plt.grid(axis="y", alpha=0.3)
        plt.tight_layout()
        plt.show()

    # 3. Korrelationsmatrix als Heatmap (nur wenn mehr als 1 Spalte)
    if numeric_df.shape[1] > 1 and numeric_df.shape[1] <= 50:
        plt.figure(figsize=(12, 10))
        corr = numeric_df.corr()

        # Achsenbeschriftungen mit Frage-Nummern
        corr_renamed = corr.copy()
        corr_renamed.columns = question_labels
        corr_renamed.index = question_labels

        sns.heatmap(
            corr_renamed,
            annot=False,
            fmt=".2f",
            cmap="coolwarm",
            square=True,
            linewidths=0.5,
            cbar_kws={"shrink": 0.8},
        )
        plt.title(
            f"Korrelationsmatrix – {fragebogen_name}", fontsize=14, fontweight="bold"
        )
        plt.tight_layout()
        plt.show()
    elif numeric_df.shape[1] > 50:
        print(
            f"Zu viele Spalten ({numeric_df.shape[1]}) für detaillierte Korrelationsmatrix - übersprungen."
        )
    else:
        print("Nur eine Spalte vorhanden – keine Korrelationsmatrix möglich.")

    # 4. ClusterMap der Korrelationsmatrix (nur wenn mehr als 1 Spalte und ≤50)
    if numeric_df.shape[1] > 1 and numeric_df.shape[1] <= 50:
        print(f"\nErstelle ClusterMap für {fragebogen_name}...")

        # Korrelationsmatrix mit umbenannten Labels
        corr_renamed = numeric_df.corr()
        corr_renamed.columns = question_labels
        corr_renamed.index = question_labels

        # NEU: NaN Werte durch 0 ersetzen für ClusterMap!
        corr_clean = corr_renamed.fillna(0)
        # ClusterMap erstellen
        g = sns.clustermap(
            corr_clean,
            cmap="coolwarm",
            center=0,
            linewidths=0.5,
            figsize=(14, 14),
            cbar_kws={"shrink": 0.8, "label": "Korrelation"},
            dendrogram_ratio=0.15,
            method="average",  # Linkage-Methode
            metric="euclidean",  # Distanzmetrik
        )

        g.fig.suptitle(
            f"ClusterMap (Hierarchisches Clustering) – {fragebogen_name}",
            fontsize=16,
            fontweight="bold",
            y=0.98,
        )
        plt.show()

        print("✓ ClusterMap erstellt - Fragen sind nach Ähnlichkeit gruppiert!")
    elif numeric_df.shape[1] > 50:
        print(
            f"Zu viele Spalten ({numeric_df.shape[1]}) für ClusterMap - übersprungen."
        )

    # Mapping-Tabelle ausgeben
    print("\n=== Mapping: Frage-Nummer → Spaltenname ===")
    for i, col in enumerate(numeric_df.columns):
        print(f"  Frage-{i+1}: {col}")


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


def plot_questionnaire_means_by_diagnosis(means_df: pd.DataFrame) -> None:
    """Plots the means of questionnaire answers based on diagnosis presence."""
    labels = [col[0] for col in means_df.columns][:-1]

    plt.bar(labels, means_df.values[0][:-1])
    plt.bar(labels, means_df.values[1][:-1])
    plt.title("Mean answers by diagnosis presence", fontsize=18)
    plt.ylabel("Mean value of the answers")
    plt.legend([means_df.index[0], means_df.index[1]])
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.show()


def main():
    # Load data
    df_metadata, df_pre_therapy_ratings, df_post_therapy_ratings = load_data()

    # Attach metadata as MultiIndex to pre-therapy ratings
    df_pre_therapy_ratings = attach_metadata_as_multiindex(
        therapy_ratings_df=df_pre_therapy_ratings.copy(),
        metadata_df=df_metadata,
        metadata_column="Variablenlabel",
    )

    # Split pre-therapy ratings by questionnaire
    pre_frageboegen = split_df_by_questionnaire(
        df_pre_therapy_ratings, df_metadata, include_diagnosis_cols=True
    )

    # Extract only RW columns
    pre_frageboegen_rw = get_rw_columns(pre_frageboegen, keep_diagnosis_cols=True)

    # Count answers per questionnaire
    answers_count = count_answers_per_fragebogen(pre_frageboegen_rw)

    # Print summary
    print("\n=== Zusammenfassung der Antworten pro Fragebogen ===")
    sorted_items = sorted(
        [(str(name), count) for name, count in answers_count.items() if pd.notna(name)],
        key=lambda x: x[1],
        reverse=True,
    )
    for name, count in sorted_items:
        print(f"  {name}: {count} Antworten")

    # Liste verfügbare Fragebögen
    print("\n=== Verfügbare Fragebögen für Detailvisualisierung ===")
    fragebogen_names = [
        str(name) for name in pre_frageboegen_rw.keys() if pd.notna(name)
    ]
    for i, name in enumerate(sorted(fragebogen_names), 1):
        print(f"  {i}. {name}")

    # Visualisiere spezifische Fragebögen
    # visualize_specific_fragebogen(pre_frageboegen_rw, "EDE-Q", normalize=True)
    # visualize_specific_fragebogen(pre_frageboegen, "PHQ-9", normalize=True)
    # visualize_specific_fragebogen(pre_frageboegen, "IIP", normalize=True)

    mean_df = get_questionnaire_means_by_diagnosis(pre_frageboegen_rw, "EDE-Q", "F33.1")

    plot_questionnaire_means_by_diagnosis(mean_df)


if __name__ == "__main__":
    main()
