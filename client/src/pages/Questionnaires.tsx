import { useEffect, useState } from "react";

function Questionnaires() {
  const [names, setNames] = useState<string[]>([]);

  useEffect(() => {
    fetch("http://localhost:5000/api/frageboegen")
      .then((res) => res.json())
      .then((data) => setNames(data))
      .catch(console.error);
  }, []);

  return (
    <div>
      <h1>Fragebögen</h1>
      <ul>
        {names.map((n) => (
          <li key={n}>{n}</li>
        ))}
      </ul>
    </div>
  );
}

export default Questionnaires;
