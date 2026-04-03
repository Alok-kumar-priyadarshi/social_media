// This component allows searching users and navigating to their profile

import { useState } from "react";
import API from "../api/axios";
import { useNavigate } from "react-router-dom";

export default function SearchBar() {
  const [query, setQuery] = useState("");
  const [results, setResults] = useState([]);
  const navigate = useNavigate();

  const handleSearch = async (e) => {
    const value = e.target.value;
    setQuery(value);

    if (!value) {
      setResults([]);
      return;
    }

    try {
      const res = await API.get(`/users/search?query=${value}`);
      setResults(res.data);
    } catch (err) {
      console.error(err);
    }
  };

  return (
    <div className="relative">
      <input
        type="text"
        placeholder="Search users..."
        value={query}
        onChange={handleSearch}
        className="border px-2 py-1 rounded w-50"
      />

      {/* Dropdown */}
      {results.length > 0 && (
        <div className="absolute bg-white border w-full mt-1 max-h-40 overflow-y-auto">
          {results.map((user) => (
            <div
              key={user.id}
              onClick={() => navigate(`/profile/${user.id}`)}
              className="p-2 hover:bg-gray-100 cursor-pointer"
            >
              {user.username}
            </div>
          ))}
        </div>
      )}
    </div>
  );
}