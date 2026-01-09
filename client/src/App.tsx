import { useEffect, useState } from 'react'
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import './App.css'

import Home from './pages/Home';
import Diagnoeses from './pages/Diagnoeses';
import Questionnaires from './pages/Questionnaires';
import Patients from './pages/Patients';
import FAQ from './pages/FAQ';

import Header from './components/Header';
import Footer from './components/Footer';

function App() {
  return (
    <Router>
      <div style={{ display: "flex", flexDirection: "column", minHeight: "100vh" }}>
        <Header />
        <main style={{ flex: "1", width: "100%", maxWidth: "1200px", margin: "0 auto", padding: "24px" }}>
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/diagnosen" element={<Diagnoeses />} />
            <Route path="/frageboegen" element={<Questionnaires />} />
            <Route path="/patienten" element={<Patients />} />
            <Route path="/faq" element={<FAQ />} />
          </Routes>
        </main>
        <Footer />
      </div>
    </Router>
  )
}

export default App
