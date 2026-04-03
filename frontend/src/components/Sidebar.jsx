// This component renders Instagram-style left sidebar navigation

import { useNavigate } from "react-router-dom";
import SearchBar from "./SearchBar";

export default function Sidebar() {
  const navigate = useNavigate();

  return (
    <div className="w-60 h-screen border-r p-4 flex flex-col justify-between fixed left-0 top-0 bg-white">
      {/* 🔥 LOGO */}
      <h1
        className="text-2xl font-bold mb-8 cursor-pointer"
        onClick={() => navigate("/")}
      >
        SocialApp
      </h1>

      {/* 🔥 NAV ITEMS */}
      <div className="flex flex-col gap-4">
        <SearchBar />

        <button
          onClick={() => navigate("/")}
          className="text-left hover:bg-gray-100 p-2 rounded"
        >
          🏠 Feed
        </button>

        <button
          onClick={() => navigate("/chat")}
          className="text-left hover:bg-gray-100 p-2 rounded"
        >
          💬 Chat
        </button>

        <button
          onClick={() => navigate("/profile")}
          className="text-left hover:bg-gray-100 p-2 rounded"
        >
          👤 Profile
        </button>

        <button
          onClick={() => navigate("/create")}
          className="text-left hover:bg-gray-100 p-2 rounded"
        >
          ➕ Create
        </button>

        <button
          onClick={() => navigate("/settings")}
          className="text-left hover:bg-gray-100 p-2 rounded"
        >
          ⚙️ Settings
        </button>
      </div>

      {/* 🔥 LOGOUT */}
      <button
        onClick={() => {
          localStorage.removeItem("token");
          navigate("/login");
        }}
        className="text-left hover:bg-red-100 p-2 rounded text-red-500"
      >
        🚪 Logout
      </button>
    </div>
  );
}
