import React from "react";
import "./Login.css";
import httpService from "../services/HttpService";

const LoginPage: React.FC = () => {
    const handleGoogleLogin = async () => {
        window.location.href = "/auth/login";
    };

    return (
        <div className="login-page">
            <div className="login-container">
                <h1>Welcome to Fintech App</h1>
                <p>Login with your Google account to continue</p>
                <button className="primary-button" onClick={handleGoogleLogin}>
                    Login with Google
                </button>
            </div>
        </div>
    );
};

export default LoginPage;
