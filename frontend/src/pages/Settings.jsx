// This page handles account settings like logout, deactivate, etc.

import { useNavigate  } from "react-router-dom";
import { useState , useEffect } from "react";   
import API from "../api/axios";

export default function Settings() {
  const navigate = useNavigate();
  const [blockedUsers, setBlockedUsers] = useState([]);

  useEffect(() => {
    API.get("/block/")
      .then((res) => setBlockedUsers(res.data))
      .catch((err) => console.error(err));
  }, []);

  // 🔥 LOGOUT
  const handleLogout = () => {
    localStorage.removeItem("token");
    navigate("/login");
  };

  // 🔥 DEACTIVATE (placeholder for now)
  const handleDeactivate = async () => {
    const confirm = window.confirm(
      "Are you sure you want to deactivate your account?",
    );
    if (!confirm) return;

    try {
      // 🚨 backend not implemented yet
      alert("Deactivate API not implemented yet");
    } catch (err) {
      console.error("Deactivate error:", err);
    }
  };

  return (
    <div className="max-w-md mx-auto p-6">
      <h2 className="text-2xl font-bold mb-6">Settings</h2>

      {/* 🔥 ACCOUNT SECTION */}
      <div className="border p-4 rounded mb-4">
        <h3 className="font-semibold mb-3">Account</h3>

        <button
          onClick={() => navigate("/edit-profile")}
          className="block w-full text-left p-2 hover:bg-gray-100 rounded"
        >
          Edit Profile
        </button>

        <button
          onClick={handleLogout}
          className="block w-full text-left p-2 hover:bg-gray-100 rounded text-red-500"
        >
          Logout
        </button>
      </div>

      <div className="border p-4 rounded mb-4">

        <h3 className="mt-6 font-semibold">Blocked Users</h3>

        {blockedUsers.length === 0 ? (
            <p className="text-gray-500">No blocked users</p>
        ) : (
            blockedUsers.map((u) => (
            <div key={u.id} className="flex justify-between p-2 border-b">
                <span>{u.username}</span>

                <button
                onClick={async () => {
                    await API.delete(`/block/${u.id}`);
                    setBlockedUsers((prev) => prev.filter((x) => x.id !== u.id));
                }}
                className="text-red-500"
                >
                Unblock
                </button>
            </div>
            ))
        )}
      </div>


      {/* 🔥 DANGER ZONE */}
      <div className="border p-4 rounded">
        <h3 className="font-semibold mb-3 text-red-500">Danger Zone</h3>

        <button
          onClick={handleDeactivate}
          className="block w-full text-left p-2 hover:bg-red-100 rounded text-red-600"
        >
          Deactivate Account
        </button>
      </div>
    </div>
  );
}
