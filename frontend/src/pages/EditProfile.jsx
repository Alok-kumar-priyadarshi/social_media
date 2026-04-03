// This page allows user to update bio + profile image properly

import { useState } from "react";
import { useNavigate } from "react-router-dom";
import API from "../api/axios";
import Navbar from "../components/Navbar";

export default function EditProfile() {
  const [bio, setBio] = useState("");
  const [file, setFile] = useState(null);
  const [preview, setPreview] = useState(null);

  const navigate = useNavigate();

  const handleFileChange = (e) => {
    const selected = e.target.files[0];
    setFile(selected);

    // 🔥 preview image instantly
    if (selected) {
      setPreview(URL.createObjectURL(selected));
    }
  };

  const handleSave = async () => {
    try {
      const formData = new FormData();

      formData.append("bio", bio);
      

      if (file) {
        formData.append("file", file);
      }

      await API.put("/users/me", formData );
      try{
          window.location.href = "/profile";

          alert("Profile updated!");
      } catch(err){
        console.error("Navigation error:", err);
      }


    } catch (err) {
      console.error("Update error:", err);
    }
  };

  return (
    <div>
      {/* <Navbar /> */}

      <div className="max-w-md mx-auto p-4">

        <h2 className="text-xl font-bold mb-4">Edit Profile</h2>

        {/* 🔥 Image Preview */}
        <div className="mb-4 flex flex-col items-center">
          <img
            src={
              preview ||
              "/assets/image.png"
            }
            className="w-24 h-24 rounded-full object-cover mb-2"
          />

          <input type="file" onChange={handleFileChange} />
        </div>

        {/* 🔥 Bio */}
        <textarea
          placeholder="Write your bio..."
          value={bio}
          onChange={(e) => setBio(e.target.value)}
          className="w-full border p-2 mb-4"
        />

        {/* 🔥 Save */}
        <button
          onClick={handleSave}
          className="bg-blue-500 text-white px-4 py-2 rounded w-full"
        >
          Save Changes
        </button>

      </div>
    </div>
  );
}