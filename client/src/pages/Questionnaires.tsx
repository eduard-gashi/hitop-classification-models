import { useEffect, useState } from "react";

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
        fetch("http://localhost:5000/api/frageboegen")
            .then((res) => res.json())
            .then((data) => setNames(data))
            .catch(console.error);
    }, []);

    useEffect(() => {
        if (!questionnaireSelected) return;

        fetch(`http://localhost:5000/api/frageboegen/${encodeURIComponent(questionnaireSelected)}`)
            .then((res) => res.json())
            .then((json: FragebogenData) => {
                console.log(json);
                setData(json);
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
