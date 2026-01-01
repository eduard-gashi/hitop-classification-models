import {
    Radar, RadarChart, PolarGrid,
    PolarAngleAxis, PolarRadiusAxis, ResponsiveContainer, Tooltip
} from "recharts";
import type { PatientData } from "../dataTypes";

export default function SpiderDiagram({ patient }: { patient: PatientData }) {
    const data = [
        { subject: "Somatoform", value: patient.scores.Somatoform_Score },
        { subject: "Internalizing", value: patient.scores.Internalizing_Score },
        { subject: "Thought Disorder", value: patient.scores.Thought_Disorder_Score},
        { subject: "Detachment", value: patient.scores.Detachment_Score },
        { subject: "Disinhibited Ext.", value: patient.scores.Disinhibited_Externalizing_Score },
        { subject: "Antagonistic Ext.", value: patient.scores.Antagonistic_Externalizing_Score },
    ];
    console.log("SpiderDiagram data:", patient);
    return (
        <div style={{ width: 600, height: 500 }}>
            <h2>Hitop Scores for Patient {patient.id}</h2>
            <ResponsiveContainer width="100%" height="100%">
                <RadarChart data={data}>
                    <PolarGrid />
                    <PolarAngleAxis dataKey="subject" />
                    <PolarRadiusAxis domain={[0, 1]} />
                    <Tooltip
                        formatter={(value: number) => value.toFixed(3)}
                        labelFormatter={(label) => `Dimension: ${label}`}
                    />
                    <Radar
                        name={`Patient ${patient.id}`}
                        dataKey="value"
                        stroke="#8884d8"
                        fill="#8884d8"
                        fillOpacity={0.6}
                    />
                </RadarChart>
            </ResponsiveContainer>
        </div>
    );
}
