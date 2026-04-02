import React from "react";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import { DashboardScreen } from "./pages/Dashboard/DashboardScreen";
import { TotemScreen } from "./pages/Totem/TotemScreen";

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        {/* Rota Padrão: Painel da Família */}
        <Route path="/" element={<DashboardScreen />} />
        
        {/* Rota do Idoso: Totem Avatar */}
        <Route path="/totem" element={<TotemScreen />} />
      </Routes>
    </BrowserRouter>
  );
}
