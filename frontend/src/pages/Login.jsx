// Better UX + navigation

import { useState } from "react";
import API from "../api/axios";
import { useNavigate } from "react-router-dom";

export default function Login() {
  const navigate = useNavigate();

  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");

const handleLogin = async () => {
    try {
        const formData = new URLSearchParams();
        formData.append("username", username);
        formData.append("password", password);

        const res = await API.post("/login", formData, {
        headers: {
            "Content-Type": "application/x-www-form-urlencoded",
        },
        });

        localStorage.setItem("token", res.data.access_token);
        navigate("/");
    } catch (err) {
        console.error(err);
        alert("Invalid credentials");
    }
};

  return (
    <div className="flex h-screen items-center justify-center bg-gray-100">
      <div className="p-6 bg-white rounded-xl shadow-lg w-80">
        <h2 className="text-xl font-bold mb-4 text-center">Login</h2>

        <input
          className="w-full p-2 border mb-2 rounded"
          placeholder="Username"
          onChange={(e) => setUsername(e.target.value)}
        />

        <input
          className="w-full p-2 border mb-4 rounded"
          type="password"
          placeholder="Password"
          onChange={(e) => setPassword(e.target.value)}
        />

        <button
          onClick={handleLogin}
          className="w-full bg-blue-500 text-white p-2 rounded hover:bg-blue-600"
        >
          Login
        </button>

        <p className="text-sm mt-3 text-center">
          Don’t have an account?{" "}
          <span
            onClick={() => navigate("/signup")}
            className="text-green-500 cursor-pointer"
          >
            Signup
          </span>
        </p>
      </div>
    </div>
  );
}