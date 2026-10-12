import { useState } from "react";
import { clearToken, getToken, saveToken } from "./auth";
import ChatPage from "./components/ChatPage";
import LoginPage from "./components/LoginPage";
import SignupPage from "./components/SignupPage";
import "./App.css";

export default function App() {
  const [token, setToken] = useState(getToken());
  const [page, setPage] = useState("login");
  const [notice, setNotice] = useState("");

  function handleLoginSuccess(newToken) {
    saveToken(newToken);
    setToken(newToken);
    setNotice("");
  }

  function handleLogout(message) {
    clearToken();
    setToken(null);
    setPage("login");
    setNotice(typeof message === "string" ? message : "");
  }

  function handleSignupSuccess() {
    setPage("login");
    setNotice("Account created. Please log in.");
  }

  if (token) {
    return <ChatPage token={token} onLogout={handleLogout} />;
  }

  if (page === "signup") {
    return (
      <SignupPage
        onSuccess={handleSignupSuccess}
        onGoToLogin={() => {
          setNotice("");
          setPage("login");
        }}
      />
    );
  }

  return (
    <LoginPage
      notice={notice}
      onSuccess={handleLoginSuccess}
      onGoToSignup={() => {
        setNotice("");
        setPage("signup");
      }}
    />
  );
}