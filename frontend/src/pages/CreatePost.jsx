// This page allows user to upload image and create a post

import { useState } from "react";
import API from "../api/axios";
import Navbar from "../components/Navbar";
import { useNavigate } from "react-router-dom";

export default function CreatePost() {
  const [file, setFile] = useState(null);
  const [caption, setCaption] = useState("");
  const navigate = useNavigate();

  const handleSubmit = async () => {
    if (!file) {
      alert("Please select an image");
      return;
    }

    try {
      // 🔹 Step 1: Upload image
      const formData = new FormData();
      formData.append("file", file);

      const uploadRes = await API.post("/upload", formData, {
        headers: { "Content-Type": "multipart/form-data" },
      });

      const imageUrl = uploadRes.data.url;

      // 🔹 Step 2: Create post
      await API.post("/posts", {
        image_url: imageUrl,
        caption: caption,
      });

      alert("Post created!");
      navigate("/profile");

    } catch (err) {
      console.error(err);
      alert("Error creating post");
    }
  };

  return (
    <div>
      {/* <Navbar /> */}

      <div className="max-w-md mx-auto p-4">

        <h2 className="text-xl font-bold mb-4">Create Post</h2>

        <input
          type="file"
          onChange={(e) => setFile(e.target.files[0])}
          className="mb-3"
        />

        <textarea
          placeholder="Write a caption..."
          value={caption}
          onChange={(e) => setCaption(e.target.value)}
          className="w-full border p-2 mb-3"
        />

        <button
          onClick={handleSubmit}
          className="bg-blue-500 text-white px-4 py-2 rounded"
        >
          Post
        </button>

      </div>
    </div>
  );
}