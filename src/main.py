import pandas as pd
from typing import Dict
from src.analysis.analysis import count_answers_per_fragebogen, calculate_statistic_significance
from src.processing.data_loader import load_data
from src.processing.metadata import attach_metadata_as_multiindex, split_df_by_questionnaire
from src.processing.preprocessing import extract_columns_from_questionnaire, add_diagnosis_presence_column
from src.visualization.plots import(
        visualize_specific_fragebogen,
        plot_means_and_p_values
)


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

    # Extract specific columns    
    pre_frageboegen_sliced = extract_columns_from_questionnaire(pre_frageboegen, rw=False, questions=True, diagnosis=True)

    # Count answers per questionnaire
    answers_count = count_answers_per_fragebogen(pre_frageboegen_sliced)

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
        str(name) for name in pre_frageboegen_sliced.keys() if pd.notna(name)
    ]
    for i, name in enumerate(sorted(fragebogen_names), 1):
        print(f"  {i}. {name}")

    # Visualisiere spezifische Fragebögen
    # visualize_specific_fragebogen(pre_frageboegen_rw, "EDE-Q", normalize=True)
    # visualize_specific_fragebogen(pre_frageboegen, "PHQ-9", normalize=True)
    # visualize_specific_fragebogen(pre_frageboegen, "IIP", normalize=True)

    df_diagnosis_presence = add_diagnosis_presence_column(pre_frageboegen_sliced, "EDE-Q", "F33.1")

    result_df = calculate_statistic_significance(df_diagnosis_presence, "F33.1")
    
    #plot_means_and_p_values(result_df)


if __name__ == "__main__":
    main()
