// This component displays followers or following list in a modal

import { useEffect, useState } from "react";
import API from "../api/axios";

export default function FollowModal({ type, userId, onClose }) {
  const [users, setUsers] = useState([]);

  useEffect(() => {
    const route =
      type === "followers"
        ? `/followers/${userId}`
        : `/following/${userId}`;

    API.get(route)
      .then((res) => setUsers(res.data))
      .catch((err) => console.error(err));
  }, [type, userId]);

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex justify-center items-center">

      <div className="bg-white w-80 max-h-400px overflow-y-auto p-4 rounded">

        <h2 className="text-lg font-bold mb-3">
          {type === "followers" ? "Followers" : "Following"}
        </h2>

        {users.map((user) => (
          <div key={user.id} className="py-2 border-b">
            {user.username}
          </div>
        ))}

        <button
          onClick={onClose}
          className="mt-4 w-full bg-gray-200 py-1 rounded"
        >
          Close
        </button>

      </div>
    </div>
  );
}