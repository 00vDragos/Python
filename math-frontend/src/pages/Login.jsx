import { useState } from "react";
import Modal from "react-modal";
import "./Login.css";
import { useNavigate } from "react-router-dom";

Modal.setAppElement("#root");

function Login() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [message, setMessage] = useState("");

  const [showModal, setShowModal] = useState(false);
  const [registerEmail, setRegisterEmail] = useState("");
  const [registerPassword, setRegisterPassword] = useState("");
  const navigate = useNavigate();

  const API_URL = import.meta.env.VITE_API_URL || "http://localhost:5000";

  const handleLogin = async (e) => {
    e.preventDefault();
    setMessage("");

    try {
      const res = await fetch(`${API_URL}/api/login`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ email, password }),
      });

      const data = await res.json();

      if (res.ok && data.access_token) {
        localStorage.setItem("token", data.access_token);
        setMessage("Login reusit!");
        navigate("/dashboard");
      } else {
        setMessage(data.error || "Eroare la autentificare.");
      }
    } catch (err) {
      console.error("Eroare la login:", err);
      setMessage("Eroare de retea sau server.");
    }
  };

  const handleRegister = async (e) => {
    e.preventDefault();
    setMessage("");

    try {
      const res = await fetch(`${API_URL}/api/register`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          email: registerEmail,
          password: registerPassword,
        }),
      });

      const data = await res.json();

      if (res.ok) {
        // Login automat dupa inregistrare
        const loginRes = await fetch(`${API_URL}/api/login`, {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            email: registerEmail,
            password: registerPassword,
          }),
        });

        const loginData = await loginRes.json();
        console.log("Autologin response:", loginData); // DEBUG

        if (loginData?.access_token) {
  localStorage.setItem("token", loginData.access_token);
  navigate("/dashboard");
} else {
  setMessage("Cont creat, dar tokenul JWT este invalid sau lipseste.");
  console.warn("Token lipsa. Raspuns login:", loginData);
}

        closeModal();
      } else {
        setMessage(data.error || data.message || "Eroare la inregistrare");
      }
    } catch (err) {
      console.error("Eroare la inregistrare:", err);
      setMessage("Eroare de retea sau server.");
    }
  };

  const closeModal = () => {
    setShowModal(false);
    setRegisterEmail("");
    setRegisterPassword("");
  };

  return (
    <div className="page-wrapper">
      <div className="login-container">
        <h2>Autentificare</h2>
        <form onSubmit={handleLogin}>
          <input
            type="email"
            placeholder="Email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
          />
          <input
            type="password"
            placeholder="Parola"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
          />
          <button type="submit">Login</button>
        </form>

        <p className="small-link">
          Nu ai cont?{" "}
          <span className="link" onClick={() => setShowModal(true)}>
            Creeaza unul
          </span>
        </p>
        <p>{message}</p>
      </div>

      <Modal
        isOpen={showModal}
        onRequestClose={closeModal}
        className="custom-modal"
        overlayClassName="modal-overlay"
      >
        <h3>Inregistrare noua</h3>
        <form onSubmit={handleRegister}>
          <input
            type="email"
            placeholder="Email"
            value={registerEmail}
            onChange={(e) => setRegisterEmail(e.target.value)}
            required
          />
          <input
            type="password"
            placeholder="Parola"
            value={registerPassword}
            onChange={(e) => setRegisterPassword(e.target.value)}
            required
          />
          <div className="modal-buttons">
            <button type="submit">Inregistreaza</button>
            <button type="button" onClick={closeModal}>
              Inchide
            </button>
          </div>
        </form>
      </Modal>
    </div>
  );
}

export default Login;
