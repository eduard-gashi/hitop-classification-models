import { useEffect, useState } from "react";
import { api } from "../apiClient";
import SpiderDiagram from "../components/SpiderDiagram";
import type { PatientData } from "../dataTypes";


export default function Patients() {
    const [patients, setPatients] = useState<Array<PatientData>>();
    const [selectedPatientId, setSelectedPatientId] = useState<number>();
    const [typedId, setTypedId] = useState<string>("");
    const MAX_PATIENT_ID = patients?.length;

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
                    diagnoses: p.diagnoses
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

    // Helper um aktuellen Patient zu finden
    const currentPatient = patients?.find(p => p.id === selectedPatientId);

    // Handler für Input/Slider Änderungen
    const handleIdChange = (val: number) => {
        setSelectedPatientId(val);
    };

    return (
        <div className="patients-page">

            <div className="patient-layout">

                {/* Spider Diagram with HiTop Scores */}
                <div className="left">
                    <div className="panel large">
                        <label style={{
                            display: 'flex',
                            alignItems: 'center',
                            gap: '10px',
                            fontWeight: 'bold',
                            borderBottom: '1px solid #eee',
                            marginBottom: '16px',
                            paddingBottom: '8px'
                        }}>
                            Patient
                            <input
                                type="number"
                                min="0"
                                value={selectedPatientId}
                                onChange={(e) => handleIdChange(Number(e.target.value))}
                                id="patientInput"
                            />
                            <input
                                type="range"
                                min="0"
                                max={MAX_PATIENT_ID}
                                value={selectedPatientId}
                                onChange={(e) => handleIdChange(Number(e.target.value))}
                                id="patientSlider"
                            />

                            <span id="patientMax" style={{ color: '#666', fontSize: '0.9em' }}>
                                (ID: {selectedPatientId})
                            </span>

                        </label>

                        <div style={{ width: '100%', height: '600px', display: 'flex', justifyContent: 'center', alignItems: 'center' }}>
                            {currentPatient ? (
                                <SpiderDiagram patient={currentPatient} />
                            ) : (
                                <div style={{ color: '#999', fontStyle: 'italic' }}>
                                    Kein Patient mit ID {selectedPatientId} gefunden.
                                </div>
                            )}
                        </div>
                    </div>
                </div>

                {/* Patients Data */}
                <div className="right panel" id="patientData">
                    <h3>Patientendaten</h3>

                    {currentPatient ? (
                        <>
                            <div style={{ marginBottom: '20px' }}>
                                <strong>ID:</strong> {currentPatient.id}
                            </div>

                            {/* Diagnoses */}
                            <div style={{ background: '#f8f9fa', padding: '15px', borderRadius: '8px', border: '1px solid #e9ecef' }}>
                                <h4 style={{ marginTop: 0, color: '#04925c' }}>Diagnosen</h4>
                                

                                {currentPatient.diagnoses && currentPatient.diagnoses.length > 0 ? (
                                    <ul style={{ paddingLeft: '20px', margin: '5px 0' }}>
                                        {currentPatient.diagnoses.map((diag, index) => (
                                            <li key={index} style={{ color: '#333' }}>
                                                {diag}
                                            </li>
                                        ))}
                                    </ul>
                                ) : (
                                    <span style={{ color: '#999', fontStyle: 'italic' }}>Keine Diagnosen vorhanden</span>
                                )}
                            </div>

                            <hr style={{ margin: '20px 0', border: 'none', borderTop: '1px solid #eee' }} />

                            {/* Debug Ansicht der Rohdaten (optional) */}
                            <details>
                                <summary style={{ cursor: 'pointer', color: '#007bff' }}>Rohdaten anzeigen</summary>
                                <pre style={{ fontSize: '0.8em', background: '#eee', padding: '10px', borderRadius: '4px', overflow: 'auto' }}>
                                    {JSON.stringify(currentPatient.scores, null, 2)}
                                </pre>
                            </details>
                        </>
                    ) : (
                        <div style={{ color: '#777', padding: '20px', textAlign: 'center' }}>
                            Bitte wählen Sie eine gültige Patienten-ID aus.
                        </div>
                    )}
                </div>
            </div>
        </div>
    );
}
