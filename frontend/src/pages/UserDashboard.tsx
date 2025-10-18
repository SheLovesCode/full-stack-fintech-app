// frontend/src/pages/UserDashboard.tsx
import React from "react";
import { useNavigate } from "react-router-dom";
import {useUser} from "./UserContext";

const UserDashboard: React.FC = () => {
    const navigate = useNavigate();
    const { user } = useUser();

    if (!user) {
        // User not loaded → redirect to login
        setTimeout(() => navigate("/login"), 100);
        return <p>Loading...</p>;
    }

    return (
        <div style={styles.container}>
            <h1>Welcome, {user.name}!</h1>
            {user.picture && <img src={user.picture} alt="Profile" style={styles.avatar} />}
            <p>Email: {user.email}</p>

            <hr style={styles.divider} />

            <h2>Payouts</h2>
            <p>Coming soon: list of payouts and create payout button.</p>
            <button style={styles.button} disabled>
                Create Payout
            </button>
        </div>
    );
};

export default UserDashboard;

const styles: { [key: string]: React.CSSProperties } = {
    container: { maxWidth: "600px", margin: "2rem auto", padding: "1rem", textAlign: "center", fontFamily: "Arial, sans-serif" },
    avatar: { width: "100px", height: "100px", borderRadius: "50%", marginTop: "1rem", marginBottom: "1rem" },
    divider: { margin: "2rem 0" },
    button: { padding: "0.75rem 1.5rem", fontSize: "1rem", borderRadius: "6px", backgroundColor: "#4CAF50", color: "#fff", border: "none", cursor: "not-allowed" },
};
