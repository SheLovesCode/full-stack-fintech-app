import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import LoginPage from "./pages/Login";
import OAuthSuccess from "./pages/OauthSuccess";
import UserDashboard from "./pages/UserDashboard";

function App() {
  return (
      <Router>
        <Routes>
            <Route path="/login" element={<LoginPage />} />
            <Route path="/auth/success" element={<OAuthSuccess />} />
            <Route path="/userDashboard" element={<UserDashboard />} />
        </Routes>
      </Router>
  );
}

export default App;
