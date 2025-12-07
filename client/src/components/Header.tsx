
export default function Header() {
    return (
        <header>
            <h1>HiTop Classification Models</h1>

            <nav
                style={{
                    display: "flex",
                    gap: "1rem",
                    borderBottom: "1px solid black",
                    paddingBottom: "1rem",
                    marginBottom: "1rem"
                }}
            >
                <a href="/">Home</a>
                <a href="/diagnosen">Diagnosen</a>
                <a href="/frageboegen">Fragebögen</a>
                <a href="/patienten">Patienten</a>
                <a href="/faq">FAQ</a>
            </nav>
        </header>
    );
}