import os
from typing import Dict
import pandas as pd
from openai import OpenAI

from backend.processing.data_loader import load_and_process_data


api_key = os.environ.get("PERPLEXITY_API_KEY")
if not api_key:
    raise RuntimeError("PERPLEXITY_API_KEY not set")

client = OpenAI(api_key=api_key, base_url="https://api.perplexity.ai")


HITOP_SPECTRA = [
    "Somatoform",
    "Internalizing",
    "Thought Disorder",
    "Detachment",
    "Disinhibited Externalizing",
    "Antagonistic Externalizing",
]


def suggest_hitop_for_questionnaire_items(fragebogen_name: str, items: list[str]) -> list[str]:
    if not items:
        return []

    items_block = "\n".join(f"{i+1}. {q}" for i, q in enumerate(items))

    prompt = f"""
Du bist Klinischer Psychologe und kennst das HiTOP-Modell.
Ordne für JEDES Item das passendste HiTOP-Hauptspektrum zu.

Mögliche Spektren:
- Somatoform
- Internalizing
- Thought Disorder
- Detachment
- Disinhibited Externalizing
- Antagonistic Externalizing

Fragebogen: {fragebogen_name}

Items (nummeriert):
{items_block}

Gib die Antwort GENAU in diesem Format zurück:
1. Internalizing
2. Somatoform
...
Nur diese Liste, keine weiteren Erklärungen.
"""

    resp = client.chat.completions.create(
        model="sonar",
        messages=[{"role": "user", "content": prompt}],
    )
    text = resp.choices[0].message.content.strip()

    lines = [l.strip() for l in text.splitlines() if l.strip()]
    spectra: list[str] = []
    for line in lines:
        parts = line.split(".", 1)  # Get Spectrum
        if len(parts) == 2:
            candidate = parts[1].strip()
        else:
            candidate = line

        matched = "Unklar"
        for spec in HITOP_SPECTRA:
            if spec.lower() in candidate.lower():
                matched = spec
                break
        spectra.append(matched)

    if len(spectra) < len(items):
        spectra += ["Unklar"] * (len(items) - len(spectra))

    return spectra[: len(items)]


def map_hitop_items(pre_fb: Dict[str, pd.DataFrame]) -> pd.DataFrame:
    columns = [
        "Fragebogen",
        "Code",
        "Frage",
        "HiTOP_Spektrum",
        "HiTOP_Spektrum_ai_suggestion",
        "HiTOP_Spektrum_secondary",
        "HiTOP_Spektrum_review",
    ]
    rows = []

    for fragebogen_name, fb in pre_fb.items():
        labels = [str(col[0]) for col in fb.columns]
        codes = [str(col[1]) for col in fb.columns]

        ai_spectra = suggest_hitop_for_questionnaire_items(fragebogen_name, labels)

        for code, label, ai_spec in zip(codes, labels, ai_spectra):
            rows.append(
                {
                    "Fragebogen": fragebogen_name,
                    "Code": code,
                    "Frage": label,
                    "HiTOP_Spektrum_ai_suggestion": ai_spec,
                    "HiTOP_Spektrum_secondary": "",
                    "HiTOP_Spektrum_review": "",
                }
            )

    return pd.DataFrame(rows, columns=columns)


if __name__ == "__main__":
    df_metadata, pre_fb, post_fb = load_and_process_data(
        data_type="processed", include_diagnosis=False
    )
    df_mapping = map_hitop_items(pre_fb)
    df_mapping.to_excel("HiTOP_Mapping_with_AI.xlsx", index=False)
    print("HiTOP_Mapping_with_AI.xlsx geschrieben")
