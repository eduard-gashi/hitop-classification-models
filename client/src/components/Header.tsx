import { Link } from "react-router-dom";

export default function Header() {
  return (
    <header>
      <h1>
        <Link to="/" style={{ fontWeight: "bold", color: "#04925c" }}>
          HiTop Classification Models
        </Link>
      </h1>
      <nav>
        <Link style={{ color: "white"}} to="/diagnosen">Diagnosen</Link>
        <Link style={{ color: "white"}} to="/frageboegen">Fragebögen</Link>
        <Link style={{ color: "white"}} to="/patienten">Patienten</Link>
        <Link style={{ color: "white"}} to="/faq">FAQ</Link>
      </nav>
    </header>
  );
}
