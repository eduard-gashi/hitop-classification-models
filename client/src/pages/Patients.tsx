import { useEffect, useState } from "react";
import { api } from "../apiClient";


type HiTopScores = {
    Somatoform_Score: number | null;
    Internalizing_Score: number | null;
    "Thought Disorder_Score": number | null;
    Detachment_Score: number | null;
    "Disinhibited Externalizing_Score": number | null;
    "Antagonistic Externalizing_Score": number | null;
};


type PatientData {
    id: number;
    scores: HiTopScores;
};


export default function Patients() {
    const [patients, setPatients] = useState<PatientData>();
    const [selectedPatientId, setSelectedPatientId] = useState<number>();


    useEffect(() => {
        console.log("HAHA");
        api.get("/api/patient_scores")
            .then((res) => {console.log(res);setPatients(res.data)})
            .catch(console.error);

    }, []);



     function getPatientData(id: number): PatientData | null {
        if (!patients) return null;
        
        // Finde den Index der ID im Array
        const index = patients.id.indexOf(id);
        if (index === -1) return null;

        // Baue das Objekt zusammen
        const scores: { [key: string]: number | null } = {};
        Object.keys(allData.scores).forEach((key) => {
            // TypeScript Cast, weil wir wissen, dass key in scores ist
            scores[key] = (allData.scores as any)[key][index];
        });

        return { id, scores };
    }

    const currentPatient = selectedPatientId ? getPatientData(selectedPatientId) : null;

    return (
        <div>
            <h1>Patienten Explorer</h1>
            
            {/* Liste */}
            <div style={{ marginBottom: "20px" }}>
                {patients?.id.map((id) => (
                    <button key={id} onClick={() => setSelectedPatientId(id)}>
                        {id}
                    </button>
                ))}
            </div>

            {/* Detailansicht (Sofort da, ohne Ladezeit!) */}
            {currentPatient && (
                <div style={{ border: "1px solid black", padding: "10px" }}>
                    <h2>Patient {currentPatient.id}</h2>
                    <pre>{JSON.stringify(currentPatient.scores, null, 2)}</pre>
                </div>
            )}
        </div>
    );
}
