import { useEffect, useState } from 'react'
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import './App.css'

import Home from './pages/Home';
import Diagnoeses from './pages/Diagnoeses';
import Questionnaires from './pages/Questionnaires';
import Patients from './pages/Patients';
import FAQ from './pages/FAQ';

import Header from './components/Header';

function App() {

  

  return (
    <Router>
      <main style={{ display: "flex", flexDirection: "column", minHeight: "90vh" }}>
        <Header />
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/diagnosen" element={<Diagnoeses/>} />
          <Route path="/frageboegen" element={<Questionnaires/>} />
          <Route path="/patienten" element={<Patients/>} />
          <Route path="/faq" element={<FAQ/>} />
        </Routes>
      </main>
    </Router>
  )
}

export default App
