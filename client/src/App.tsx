import { useState } from 'react'
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import './App.css'

import Home from './pages/Home';


function App() {

  return (
    <Router>
      <main style={{ display: "flex", flexDirection: "column", minHeight: "90vh" }}>
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/diagnosen" element={<div>About Page</div>} />
          <Route path="/frageboegen" element={<div>Fragebogen Explorer</div>} />
          <Route path="/patienten" element={<div>Fragebogen Explorer</div>} />
          <Route path="/faq" element={<div>Fragebogen Explorer</div>} />
        </Routes>
      </main>
    </Router>
  )
}

export default App
