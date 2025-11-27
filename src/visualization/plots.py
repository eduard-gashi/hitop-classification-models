import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd
from typing import Dict, Tuple, Optional
from sklearn.preprocessing import StandardScaler

def visualize_specific_fragebogen(
    frageboegen: Dict[str, pd.DataFrame], fragebogen_name: str, normalize=True
):
    """
    Hauptfunktion: Koordiniert die Visualisierung eines spezifischen Fragebogens.
    """
    # 1. Datenvorbereitung & Validierung
    data = _prepare_data(frageboegen, fragebogen_name)
    if data is None:
        return
    
    numeric_df, numeric_df_renamed, question_labels = data

    # 2. Statistiken ausgeben
    _print_stats(fragebogen_name, numeric_df)

    # 3. Visualisierungen aufrufen
    #_plot_histograms(numeric_df_renamed, fragebogen_name)
    #_plot_boxplots(numeric_df_renamed, fragebogen_name, normalize)
    
    # Korrelationen nur plotten, wenn sinnvoll (mehr als 1 Spalte, nicht zu viele)
    n_cols = numeric_df.shape[1]
    if 1 < n_cols <= 50:
        #_plot_correlation_heatmap(numeric_df_renamed, fragebogen_name)
        _plot_clustermap(numeric_df_renamed, fragebogen_name)
    elif n_cols > 50:
        print(f"Zu viele Spalten ({n_cols}) für Korrelationsplots - übersprungen.")
    else:
        print("Nur eine Spalte vorhanden – keine Korrelationsmatrix möglich.")

    # 4. Mapping ausgeben
    _print_mapping(numeric_df)


# --- HILFSFUNKTIONEN ---

def _prepare_data(
    frageboegen: Dict[str, pd.DataFrame], name: str
) -> Optional[Tuple[pd.DataFrame, pd.DataFrame, list]]:
    """Extrahiert numerische Daten und erstellt Labels."""
    if name not in frageboegen:
        print(f"Fehler: Fragebogen '{name}' nicht gefunden!")
        print(f"Verfügbare Fragebögen: {list(frageboegen.keys())}")
        return None

    df = frageboegen[name]
    numeric_df = df.select_dtypes(include="number")

    if numeric_df.empty:
        print(f"{name}: Keine numerischen Daten vorhanden.")
        return None

    # Labels generieren und DF umbenennen
    question_labels = [f"Frage-{i+1}" for i in range(numeric_df.shape[1])]
    numeric_df_renamed = numeric_df.copy()
    numeric_df_renamed.columns = question_labels

    return numeric_df, numeric_df_renamed, question_labels


def _print_stats(name: str, df: pd.DataFrame):
    """Gibt Basis-Statistiken aus."""
    print(f"\n=== Visualisierung: {name} ===")
    print(f"Shape: {df.shape}")
    print(f"Anzahl Spalten: {df.shape[1]}")
    print(f"Anzahl Zeilen: {df.shape[0]}\n")


def _plot_histograms(df: pd.DataFrame, name: str):
    """Erstellt das Histogramm-Grid."""
    n_cols = df.shape[1]
    n_rows = int(np.ceil(n_cols / 4))

    fig, axes = plt.subplots(n_rows, 4, figsize=(16, 4 * n_rows))
    axes_flat = axes.flatten() if n_cols > 1 else [axes]

    for i, col in enumerate(df.columns):
        ax = axes_flat[i]
        ax.hist(
            df[col].dropna(),
            bins=20,
            edgecolor="black",
            color="steelblue",
        )
        ax.set_title(col, fontsize=10)
        ax.set_xlabel("Wert")
        ax.set_ylabel("Häufigkeit")
        ax.grid(alpha=0.3)

    # Leere Subplots ausblenden
    for i in range(n_cols, len(axes_flat)):
        axes_flat[i].set_visible(False)

    plt.suptitle(f"Histogramme – {name}", fontsize=16, fontweight="bold")
    plt.tight_layout()
    plt.show()


def _plot_boxplots(df: pd.DataFrame, name: str, normalize: bool):
    """Erstellt Boxplots (optional mit Normalisierung)."""
    if not normalize:
        # Einfacher Plot
        plt.figure(figsize=(16, 6))
        df.plot(kind="box", ax=plt.gca())
        plt.title(f"Boxplot – {name}", fontsize=14, fontweight="bold")
        plt.xticks(rotation=45, ha="right")
        plt.grid(axis="y", alpha=0.3)
        plt.tight_layout()
        plt.show()
        return

    # Mit Normalisierung
    scaler = StandardScaler()
    normalized_values = scaler.fit_transform(df.dropna())
    normalized_df = pd.DataFrame(normalized_values, columns=df.columns)

    fig, axes = plt.subplots(2, 1, figsize=(16, 12))

    # Original
    df.plot(kind="box", ax=axes[0])
    axes[0].set_title(f"Boxplot (Original) – {name}", fontsize=14, fontweight="bold")
    axes[0].grid(axis="y", alpha=0.3)
    axes[0].tick_params(axis="x", rotation=45)

    # Normalisiert
    normalized_df.plot(kind="box", ax=axes[1])
    axes[1].set_title(f"Boxplot (Z-Score normalisiert) – {name}", fontsize=14, fontweight="bold")
    axes[1].set_ylabel("Std. Werte (M=0, SD=1)")
    axes[1].grid(axis="y", alpha=0.3)
    axes[1].tick_params(axis="x", rotation=45)

    plt.tight_layout()
    plt.show()


def _plot_correlation_heatmap(df: pd.DataFrame, name: str):
    plt.figure(figsize=(12, 10))
    corr = df.corr()

    sns.heatmap(
        corr,
        annot=False,
        fmt=".2f",
        cmap="RdBu_r",     # <--- Stärkerer Kontrast (Rot/Blau)
        center=0,          # <--- Zwingt 0 auf Weiß (wichtig!)
        vmin=-1, vmax=1,   # <--- Skala fixieren (-1 bis 1)
        square=True,
        linewidths=0.5,
        cbar_kws={"shrink": 0.8},
    )
    plt.title(f"Korrelationsmatrix – {name}", fontsize=14, fontweight="bold")
    plt.tight_layout()
    plt.show()



def _plot_clustermap(df: pd.DataFrame, name: str):
    """Erstellt die hierarchische ClusterMap."""
    print(f"\nErstelle ClusterMap für {name}...")
    
    # NaN durch 0 ersetzen für Clustering
    corr_clean = df.corr().fillna(0)
    
    g = sns.clustermap(
        corr_clean,
        cmap="coolwarm",
        center=0,
        linewidths=0.5,
        figsize=(14, 14),
        cbar_kws={"shrink": 0.8, "label": "Korrelation"},
        dendrogram_ratio=0.15,
        method="average",
        metric="euclidean",
    )
    
    g.fig.suptitle(
        f"ClusterMap (Hierarchisches Clustering) – {name}",
        fontsize=16,
        fontweight="bold",
        y=0.98,
    )
    plt.show()
    print("✓ ClusterMap erstellt - Fragen sind nach Ähnlichkeit gruppiert!")


def _print_mapping(original_df: pd.DataFrame):
    """Gibt das Mapping der Spaltennamen aus."""
    print("\n=== Mapping: Frage-Nummer → Spaltenname ===")
    for i, col in enumerate(original_df.columns):
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


def plot_histogram_overview(df: pd.DataFrame, name: str):
    plt.figure(figsize=(10, 6))
    
    # Plottet alle Spalten übereinander (gut für die Gesamtverteilung des Fragebogens)
    sns.histplot(
        df.melt(), 
        x="value", 
        kde=True, # Zeigt die Kurve
        bins=30,
        color="teal"
    )
    
    plt.title(f"Gesamtverteilung der Antworten – {name}", fontsize=14)
    plt.xlabel("Z-Score")
    plt.ylabel("Häufigkeit")
    plt.show()


def plot_answer_distributions(df: pd.DataFrame, name: str):
    """Zeigt die Verteilung der z-standardisierten Antworten für alle Items."""
    
    # Daten ins "Long Format" bringen (nötig für Seaborn FacetGrid)
    # id_vars=[] weil wir keine ID Spalte haben, alles sind Messwerte
    df_long = df.melt(var_name="Item", value_name="Z-Score")
    
    plt.figure(figsize=(12, 8))
    
    # Ein Violinplot zeigt die Dichte UND die Streuung perfekt
    sns.violinplot(
        data=df_long,
        x="Z-Score",
        y="Item",
        orient="h", # Horizontal ist besser lesbar bei vielen Items
        palette="viridis",
        inner="quartile" # Zeigt Median und Quartile als Striche
    )
    
    plt.title(f"Antwortverteilung (Z-Scores) – {name}", fontsize=14, fontweight="bold")
    plt.xlabel("Z-Score (0 = Durchschnitt)", fontsize=12)
    plt.ylabel("Fragebogen Items", fontsize=12)
    plt.axvline(0, color="black", linestyle="--", alpha=0.5) # Nulllinie zur Orientierung
    plt.tight_layout()
    plt.show()

# Aufruf:
# plot_answer_distributions(dfs_dict["SAS"], "SAS")
