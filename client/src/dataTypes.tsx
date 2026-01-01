export type HiTopScores = {
    Somatoform_Score: number | null;
    Internalizing_Score: number | null;
    Thought_Disorder_Score: number | null;
    Detachment_Score: number | null;
    Disinhibited_Externalizing_Score: number | null;
    Antagonistic_Externalizing_Score: number | null;
};


export type PatientData = {
    id: number;
    scores: HiTopScores;
};