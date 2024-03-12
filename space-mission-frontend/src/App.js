import React from 'react';
import { Route, Routes } from "react-router-dom";
import Login from './components/Login.js';
import Home from "./components/Home.js";

function App() {
  return (
    <div>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/login" element={<Login/>} />
      </Routes>
    </div>
  );
}

export default App;
