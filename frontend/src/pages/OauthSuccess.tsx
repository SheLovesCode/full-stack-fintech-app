// frontend/src/pages/OAuthSuccess.tsx
import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import {useUser} from "./UserContext";
import API_URL from "../config/Config";

const OAuthSuccess: React.FC = () => {
    const navigate = useNavigate();
    const { setUser } = useUser();
    const [message, setMessage] = useState("Authentication successful! Redirecting to your dashboard...");

    useEffect(() => {
        const handleOAuth = async () => {
            const params = new URLSearchParams(window.location.search);
            const token = params.get("access_token");

            if (!token) {
                setMessage("Authentication failed. Redirecting to login...");
                setTimeout(() => navigate("/login"), 2000);
                return;
            }

            // Store JWT in localStorage
            localStorage.setItem("app_jwt", token);

            try {
                // Fetch user profile from backend
                const res = await fetch(`${API_URL}/auth/me`, {
                    headers: { Authorization: `Bearer ${token}` },
                });

                if (!res.ok) throw new Error("Failed to fetch user profile");
                const data = await res.json();
                setUser(data); // store in context
            } catch (err) {
                console.error(err);
                setMessage("Failed to fetch profile. Redirecting to login...");
                localStorage.removeItem("app_jwt");
                setTimeout(() => navigate("/login"), 2000);
                return;
            }

            setTimeout(() => navigate("/userDashboard"), 1500);
        };

        handleOAuth();
    }, [navigate, setUser]);

    return (
        <div style={styles.container}>
            <div style={styles.box}>
                <h2>{message}</h2>
                <p>Please wait...</p>
            </div>
        </div>
    );
};

export default OAuthSuccess;

const styles: { [key: string]: React.CSSProperties } = {
    container: { display: "flex", height: "100vh", alignItems: "center", justifyContent: "center", backgroundColor: "#f7f9fc" },
    box: { padding: "2rem", borderRadius: "8px", backgroundColor: "#fff", boxShadow: "0 4px 12px rgba(0,0,0,0.1)", textAlign: "center" },
};
