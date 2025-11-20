import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd
from typing import Dict
from sklearn.preprocessing import StandardScaler

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


def plot_means_and_p_values(df: pd.DataFrame) -> None:
    """Plots the means and p-values of questionnaire answers based on diagnosis presence."""
    df = df[:-1]
    questions = df['question'].values
    labels = [question[0] for question in questions]
    N = len(labels)
    x = np.arange(N)
    width = 0.35

    plt.bar(x - width/2, df['mean_true'].values, width=width, label="Diagnose vorhanden")
    plt.bar(x + width/2, df['mean_false'].values, width=width, label="Diagnose nicht vorhanden")
    plt.title("Mittelwerte nach Diagnose", fontsize=18)
    plt.ylabel("Mittelwert der Frageantworten")
    plt.xticks(x, labels, rotation=45, ha="right")
    plt.legend()
    
    # Show the p-values above the bars
    ymax = max(np.max(df['mean_true'].values), np.max(df['mean_false'].values))
    label_offset = ymax + 0.04*ymax

    for i, p in enumerate(df['p_value'].values):
        plt.text(x[i], label_offset, f"p = {p:.3f}", ha="center", va="top", fontsize=10, color="green", rotation=0)

    plt.tight_layout()
    plt.show()
