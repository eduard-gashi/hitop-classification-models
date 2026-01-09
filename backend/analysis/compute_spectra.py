import pandas as pd
from scipy.stats import norm

from backend.processing.data_loader import load_data
from backend.config import HITOP_SPECTRA


def _clean_data(data):
    """
    Clean and normalize the HiTOP mapping DataFrame.

    Parameters
    ----------
    data : pandas.DataFrame
        Raw mapping table.

    Returns
    -------
    pandas.DataFrame
        Cleaned table with irrelevant rows removed, labels standardized, and a filled `Mapping` column.
    """

    # 'Code', 'HiTOP_Spektrum_ai_suggestion', 'Finn', 'Tim'
    data = data.drop(columns = ['Fragebogen', 'Spalte1', 'Frage', 'HiTOP_Spektrum'])
    data = data.rename(columns = {'HiTOP_Spektrum_ai_suggestion' : 'Suggested'})

    # Raus Masken
    mask_finn = ~data['Finn'].astype('string').str.contains(r'\braus\b', case = False, na = False)
    mask_tim = ~data['Tim'].astype('string').str.contains(r'\braus\b', case = False, na = False)
    # Unwichtige/Irrelevante Fragen mit den Masken herausfiltern
    data = data[mask_finn & mask_tim]

    # Finn und Tim zu einer Spalte zusammenfassen
    data['Mapping'] = (
        data["Finn"].astype("string")
        .str.cat(data["Tim"].astype("string"), sep="", na_rep="")
        .replace("", pd.NA)
    )
    data["Mapping"] = (data["Mapping"].astype("string").replace({r"^[\s?]*\?[\s?]*$": pd.NA}, regex=True))
    
    data['Mapping'] = data['Mapping'].astype('string').replace(r'\bInternalising\b', 'Internalizing', regex = True)
    data['Mapping'] = data['Mapping'].astype('string').replace(r'\bDisinhibiton\b', 'Disinhibition', regex = True)
    data['Mapping'] = data['Mapping'].astype('string').replace(r'\bDisinhibiton\b', 'Disinhibited Externalizing', regex = True)
    data['Mapping'] = data['Mapping'].astype('string').replace(r'\bAntagonism\b', 'Antagonistic Externalizing', regex = True)
    data['Mapping'] = data['Mapping'].astype('string').replace(r'.*Antagnositc Externalising\b', 'Antagonistic Externalizing', regex = True)
    data['Mapping'] = data['Mapping'].astype('string').replace(r'\bAntisocial Behavior\b', 'Disinhibited Externalizing + Antagonistic Externalizing', regex = True)
    data['Mapping'] = data['Mapping'].astype('string').str.strip()
    data['Suggested'] = data['Suggested'].astype('string').str.strip()

    # Spalten kombinieren (Falls kein Wert vorhanden dann Suggested)
    data['Mapping'] = data['Mapping'].combine_first(data['Suggested'])
    
    return data


def get_spectra_codes() -> dict[str, list]:
    """
    Build a mapping from HiTOP spectra to the corresponding question codes.

    The function cleans the input data via `_clean_data`, then creates one boolean column per
    spectrum in `HITOP_SPECTRA` by checking whether the (standardized) `Mapping` string contains
    the spectrum label. Finally, it returns a dictionary where each spectrum maps to the list of
    `Code` values for rows that matched that spectrum.

    Parameters
    ----------
    data : pandas.DataFrame
        Raw input DataFrame with question `Code` and mapping information (Finn/Tim/Suggested).

    Returns
    -------
    dict[str, list]
        Dictionary of the form `{spectrum: [code1, code2, ...]}` in the order of `HITOP_SPECTRA`.
    """
    _, data, _ = load_data()

    # Rechtschreibung, Spalten zusammenfassen, Diagnosen vereinheitlichen
    data = _clean_data(data)

    # Spalten der Spektra hinzufügen und als True/False mappen
    for spectrum in HITOP_SPECTRA:
        pattern = rf'\b{spectrum}\b'
        data[spectrum] = data['Mapping'].astype('string').str.contains(pattern, case = False, na = False)

    # Codes extrahieren für jedes Spektrum
    keys = HITOP_SPECTRA
    values = [data[data[x] == True]['Code'] for x in HITOP_SPECTRA]

    spectra_dict = dict(zip(keys, values))

    return spectra_dict


def calculate_scores() -> pd.DataFrame:
    """
    Calculates the overall scores for each spectra.
    Uses the get_spectra_codes function to access the mapping of each code to a HiTop-spectra. Averages the HiTop-spectra and negates
    inverse questions. Turns the outcome of each patient into a probability between 0 and 1 with
    """
    mapping = get_spectra_codes()
    polung = mapping.pop("Umpolen").values
    polung = [f"z_{col}" for col in polung]
    
    _, pre_dataset, _ = load_data("standardized")

    for spectrum, columns in mapping.items():
        valid_cols = [f"z_{col}" for col in columns if f"z_{col}" in pre_dataset.columns and "rw" not in col]

        if valid_cols:
            # Negate inverse questions
            for col in polung:
                if col in valid_cols:
                    pre_dataset[col] = -pre_dataset[col]
            
            # Compute mean value across all codes for the spectrum
            z_mean = pre_dataset[valid_cols].mean(axis=1)

            # Compute probability
            pre_dataset[f"{spectrum}_Score"] = norm.cdf(z_mean)

            # Raw mean value
            pre_dataset[f"{spectrum}_Z_Score"] = z_mean
        else:
            print(f"Warning: No valid columns found for spectrum '{spectrum}'")

    return pre_dataset

if __name__ == "__main__":
    calculate_scores()
