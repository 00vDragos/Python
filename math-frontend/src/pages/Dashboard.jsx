import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";

function Dashboard() {
  const navigate = useNavigate();
  const [token, setToken] = useState("");
  const [operation, setOperation] = useState("fibonacci");
  const [inputs, setInputs] = useState({ n: "", base: "", exponent: "" });
  const [result, setResult] = useState(null);
  const [error, setError] = useState("");
  const [fromCache, setFromCache] = useState(false);
  const API_URL = import.meta.env.VITE_API_URL || "http://localhost:5000";

  useEffect(() => {
    const savedToken = localStorage.getItem("token");
    if (!savedToken || savedToken === "undefined") {
      navigate("/login");
    } else {
      setToken(savedToken);
    }
  }, [navigate]);

  const handleLogout = () => {
    localStorage.removeItem("token");
    navigate("/login");
  };

  const handleChange = (e) => {
    setInputs({ ...inputs, [e.target.name]: e.target.value });
  };

  const handleCalculate = async () => {
    setResult(null);
    setError("");
    setFromCache(false);

    if (!token || token === "undefined") {
      setError("Token JWT lipsa sau invalid. Te rugam sa te reconectezi.");
      return;
    }

    let endpoint = "";
    let body = {};

    switch (operation) {
      case "fibonacci":
      case "factorial":
        endpoint = `/api/${operation}`;
        body = { n: parseInt(inputs.n) };
        if (body.n < 0 || isNaN(body.n)) {
          setError("Numarul trebuie sa fie mai mare decat 0");
          return;
        }
        break;
      case "pow":
        endpoint = "/api/pow";
        body = {
          base: parseFloat(inputs.base),
          exponent: parseFloat(inputs.exponent),
        };
        if (
          body.base < 0 ||
          body.exponent < 0 ||
          isNaN(body.base) ||
          isNaN(body.exponent)
        ) {
          setError("Numarul trebuie sa fie mai mare decat 0");
          return;
        }
        break;
      default:
        setError("Operatie necunoscuta.");
        return;
    }

    try {
      console.log("Trimis la backend:", endpoint, body);

      const res = await fetch(`${API_URL}${endpoint}`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify(body),
      });

      const data = await res.json();
      console.log("Raspuns backend:", data);

      if (res.ok) {
        setResult(data.result);
        setFromCache(data.from_cache === true);
      } else {
        if (Array.isArray(data.error)) {
          const msg = data.error[0]?.msg || "Eroare de validare.";
          setError(msg);
        } else if (typeof data.error === "string") {
          if (
            data.error.includes("pozitiv") ||
            data.error.includes("mai mare")
          ) {
            setError("Numarul trebuie sa fie mai mare decat 0");
          } else {
            setError(data.error);
          }
        } else {
          setError("Eroare necunoscuta.");
        }
      }
    } catch (err) {
      console.error("Eroare retea/backend:", err);
      setError("Eroare de retea/server.");
    }
  };

  return (
    <div className="page-wrapper">
      <div className="login-container">
        <h2>Calculator</h2>

        <div style={{ textAlign: "left", marginBottom: 20 }}>
          <label>
            <input
              type="radio"
              name="operation"
              value="fibonacci"
              checked={operation === "fibonacci"}
              onChange={() => setOperation("fibonacci")}
            />
            Fibonacci
          </label>
          <br />
          <label>
            <input
              type="radio"
              name="operation"
              value="factorial"
              checked={operation === "factorial"}
              onChange={() => setOperation("factorial")}
            />
            Factorial
          </label>
          <br />
          <label>
            <input
              type="radio"
              name="operation"
              value="pow"
              checked={operation === "pow"}
              onChange={() => setOperation("pow")}
            />
            Ridicare la putere
          </label>
        </div>

        {operation === "pow" ? (
          <>
            <input
              type="number"
              name="base"
              placeholder="Base"
              value={inputs.base}
              onChange={handleChange}
              required
            />
            <input
              type="number"
              name="exponent"
              placeholder="Exponent"
              value={inputs.exponent}
              onChange={handleChange}
              required
            />
          </>
        ) : (
          <input
            type="number"
            name="n"
            placeholder="n"
            value={inputs.n}
            onChange={handleChange}
            required
          />
        )}

        <button onClick={handleCalculate}>Calculeaza</button>

        {result !== null && (
          <p style={{ marginTop: 15 }}>
            Rezultat: <strong>{result}</strong>
            {fromCache && (
              <span style={{ color: "green", marginLeft: 10 }}>
                (preluat din cache)
              </span>
            )}
          </p>
        )}

        {error && (
          <p style={{ color: "red", marginTop: 15 }}>{error}</p>
        )}

        <hr style={{ margin: "30px 0" }} />
        <button onClick={handleLogout}>Logout</button>
      </div>
    </div>
  );
}

export default Dashboard;
