import { useEffect, useState } from "react";
import { api } from "../apiClient";
import SpiderDiagram from "../components/SpiderDiagram";
import type { PatientData } from "../dataTypes";


export default function Patients() {
    const [patients, setPatients] = useState<Array<PatientData>>();
    const [selectedPatientId, setSelectedPatientId] = useState<number>();
    const [typedId, setTypedId] = useState<string>("");

    useEffect(() => {
        const idNum = Number(typedId);
        if (!Number.isNaN(idNum)) {
            setSelectedPatientId(idNum);
        } else {
            setSelectedPatientId(undefined);
        }
    }, [typedId]);

    useEffect(() => {
        api.get("/api/patient_scores")
            .then((res) => {
                console.log("Fetched patient scores:", res.data);
                const mapped: PatientData[] = res.data.map((p: any) => ({
                    id: p.id,
                    scores: {
                        Somatoform_Score: p["Somatoform_Score"],
                        Internalizing_Score: p["Internalizing_Score"],
                        Thought_Disorder_Score: p["Thought Disorder_Score"],
                        Detachment_Score: p["Detachment_Score"],
                        Disinhibited_Externalizing_Score: p["Disinhibited Externalizing_Score"],
                        Antagonistic_Externalizing_Score: p["Antagonistic Externalizing_Score"],
                    },
                }));
                setPatients(mapped);
            })
            .catch((err) => {
                console.error("Error fetching patient scores:", err);
            });
    }, []);

    function getPatientData(id: number): PatientData | null {
        if (!patients) return null;

        // Find the patient with the given id
        for (let i = 0; i < patients.length; i++) {
            if (patients[i].id === id) {
                console.log("Found patient:", patients[i]);
                return patients[i];
            }
        }
        return null;
    }

    const currentPatient = selectedPatientId ? getPatientData(selectedPatientId) : null;

    return (
        <div className="patients-page">
            <div style={{ display: "flex", flexDirection: "row", justifyContent: "center", gap: "50px" }}>
                <h1 style={{ justifyContent: "center", display: "flex", fontSize: "2.5rem" }}>
                    Patienten Explorer
                </h1>

                {/* Select patient */}
                <div className="patient-selector">
                    <input
                        type="number"
                        value={typedId}
                        onChange={(e) => setTypedId(e.target.value)}
                        placeholder="Patienten-ID eingeben..."
                        style={{ width: 300 }}
                    />

                </div>
            </div>

            {/* Details */}
            {
                currentPatient && (
                    <div className="patient-details">
                        <SpiderDiagram patient={currentPatient} />
                    </div>
                )
            }
        </div>
    );
}
