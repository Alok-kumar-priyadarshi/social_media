// Top navigation bar

import { useNavigate } from "react-router-dom";
import SearchBar from "./SearchBar";

export default function Navbar() {
  const navigate = useNavigate();

  const logout = () => {
    localStorage.removeItem("token");
    navigate("/login");
  };

  return (
    <div className="flex justify-between items-center p-4 border-b bg-white">
      <h1
        onClick={() => navigate("/")}
        className="font-bold text-lg cursor-pointer"
      >
        SocialApp
      </h1>

      <div className="flex gap-4">
        <button onClick={() => navigate("/")}>Feed</button>
        <button onClick={() => navigate("/chat")}>Chat</button>
        <button onClick={logout} className="text-red-500">
          Logout
        </button>
        <button onClick={() => navigate("/profile")}>Profile</button>

        <SearchBar />

        <button onClick={() => navigate("/create")}>
        Create
        </button>


      </div>
    </div>
  );
}