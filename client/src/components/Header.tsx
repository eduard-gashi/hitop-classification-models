import { NavLink } from "react-router-dom";
import mindePulseLogo from '../assets/logo1.png';

export default function Header() {
  return (
    <header>
      <div className="header">
        {/* Logo & Title  */}
        <div className="header-brand">
          <img src={mindePulseLogo} className="header-logo"></img>
          <h1>MindPulse</h1>
        </div>

        {/* Navigation Tabs */}
        <nav>
          <NavLink
            to="/"
            end
            className={({ isActive }) => isActive ? "tab active" : "tab"}
          >
            Start
          </NavLink>

          <NavLink
            to="/patienten"
            className={({ isActive }) => isActive ? "tab active" : "tab"}
          >
            Patient
          </NavLink>

          <NavLink
            to="/diagnosen"
            className={({ isActive }) => isActive ? "tab active" : "tab"}
          >
            Cluster
          </NavLink>

          <NavLink
            to="/prognose"
            className="tab disabled"
            onClick={(e) => e.preventDefault()}
          >
            Verlauf / Prognose
          </NavLink>

          <NavLink
            to="/frageboegen"
            className={({ isActive }) => isActive ? "tab active" : "tab"}
          >
            Fragebogen
          </NavLink>

          <NavLink
            to="/faq"
            className={({ isActive }) => isActive ? "tab active" : "tab"}
          >
            Auswertung
          </NavLink>
        </nav>
      </div>
    </header>
  );
}
