import { useEffect, useState } from "react";
import { api } from "../apiClient";


type FragebogenData = {
    name: string;
    columns: string[];
    data: { [col: string]: number | string | null }[];
};


function Questionnaires() {
    const [names, setNames] = useState<string[]>([]);
    const [questionnaireSelected, setQuestionnaireSelected] = useState<string>("");
    const [data, setData] = useState<FragebogenData | null>(null);

    useEffect(() => {
        api.get("/api/frageboegen")
            .then((res) => setNames(res.data))
            .catch(console.error);
            
    }, []);

    useEffect(() => {
        if (!questionnaireSelected) return;

        api.get(`/api/frageboegen/${encodeURIComponent(questionnaireSelected)}`)
            .then((res) => {
                console.log(res.data);
                setData(res.data);
            })
            .catch(console.error);
    }, [questionnaireSelected]);

    function handleBackToOverview() {
        setQuestionnaireSelected("");
        setData(null);
    }

    return (
        <div>
            <h1>Fragebögen</h1>

            {!data && (
                <ul>
                    {names.map((n) => (
                        <li key={n}>
                            <button onClick={() => setQuestionnaireSelected(n)}>
                                {n}
                            </button>
                        </li>
                    ))}
                </ul>
            )}

            {data && (
                <div style={{ marginTop: "1rem" }}>
                    <h2>{data.name}</h2>
                    <p>Spalten / Items:</p>
                    <ul>
                        {data.columns.map((c) => (
                            <li key={c}>{c}</li>
                        ))}
                    </ul>
                    <button onClick={handleBackToOverview}>
                        Zur Übersicht
                    </button>
                </div>
            )}
        </div>
    );
}



export default Questionnaires;
