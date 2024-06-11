import React from "react";
import TablePage from "./TablePage";
import { BrowserRouter, Routes, Route } from "react-router-dom";

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<TablePage />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
