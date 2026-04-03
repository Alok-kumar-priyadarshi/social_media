// This page displays feed posts with correct pagination (clean version)

import { useEffect, useState } from "react";
import API from "../api/axios";
import Navbar from "../components/Navbar";

export default function Feed() {
  const [posts, setPosts] = useState([]);
  const [offset, setOffset] = useState(0);
  const [loading, setLoading] = useState(false);
  const [comments, setComments] = useState({});
  const [newComment, setNewComment] = useState("");
  const [visibleComments, setVisibleComments] = useState({});

  const limit = 20;

  const handleLike = async (postId, isLiked) => {
    try {
      if (isLiked) {
        await API.delete(`/likes/${postId}`);
      } else {
        await API.post(`/likes/${postId}`);
      }

      //  update UI instantly
      setPosts((prev) =>
        prev.map((p) =>
          p.id === postId
            ? {
                ...p,
                is_liked: !isLiked,
                like_count: isLiked ? p.like_count - 1 : p.like_count + 1,
              }
            : p,
        ),
      );
    } catch (err) {
      console.error("Like error:", err);
    }
  };

  const loadPosts = async () => {
    if (loading) return;

    setLoading(true);

    try {
    //   console.log("CALLING API WITH OFFSET:", offset);

      const res = await API.get(`/posts/feed?offset=${offset}&limit=${limit}`);

    //   console.log("RESPONSE:", res.data);

      // 🔥 append new posts
      setPosts((prev) => [...prev, ...res.data]);

      // 🔥 update offset correctly
      setOffset((prev) => prev + limit);
    } catch (err) {
      console.error("Feed error:", err);
    }

    setLoading(false);
  };

  // 🔹 initial load
  useEffect(() => {
    loadPosts();
  }, []);

  // 🔹 infinite scroll
  useEffect(() => {
    const handleScroll = () => {
      const nearBottom =
        window.innerHeight + document.documentElement.scrollTop >=
        document.documentElement.offsetHeight - 100;

      if (nearBottom && !loading) {
        loadPosts();
      }
    };

    window.addEventListener("scroll", handleScroll);
    return () => window.removeEventListener("scroll", handleScroll);
  }, [offset, loading]);

  const loadComments = async (postId) => {
    const res = await API.get(`/comments/${postId}`);
    setComments((prev) => ({
      ...prev,
      [postId]: res.data,
    }));
  };

  const handleComment = async (postId) => {
    const content = newComment[postId];
    if (!content) return;

    await API.post(`/comments/${postId}?content=${content}`);

    setNewComment((prev) => ({
      ...prev,
      [postId]: "",
    }));

    toggleComments(postId); // refresh
  };

  const toggleComments = async (postId) => {
    if (!visibleComments[postId]) {
      const res = await API.get(`/comments/${postId}`);

      setComments((prev) => ({
        ...prev,
        [postId]: res.data,
      }));
    }

    setVisibleComments((prev) => ({
      ...prev,
      [postId]: !prev[postId],
    }));
  };

  return (
    <div>
      {/* <Navbar /> */}

      <div className="max-w-xl mx-auto p-4">
        {posts.length === 0 && (
          <div>No posts yet. Follow users to see content.</div>
        )}

        {posts.map((post) => (
          <div key={post.id} className="mb-6 border rounded p-3">
            <img
              src={post.image_url}
              className="w-full max-h-96 object-cover mb-2"
            />

            <p className="font-semibold">{post.username}</p>

            {/* <p className="font-semibold">User {post.user_id}</p> */}
            <p>{post.caption}</p>

            <button
              onClick={() => handleLike(post.id, post.is_liked)}
              className="flex items-center gap-2 mt-2"
            >
              <span style={{ fontSize: "20px" }}>
                {post.is_liked ? "❤️" : "🤍"}
              </span>

              <span>{post.is_liked ? "Unlike" : "Like"}</span>
            </button>

            <p>{post.like_count} likes</p>

            <div className="mt-3">
              <button
                onClick={() => toggleComments(post.id)}
                className="text-sm text-gray-500"
              >
                {visibleComments[post.id] ? "Hide Comments" : "View Comments"}
              </button>


              <div>
                  <input
                    value={newComment[post.id] || ""}
                    onChange={(e) =>
                      setNewComment((prev) => ({
                        ...prev,
                        [post.id]: e.target.value,
                      }))
                    }
                    placeholder="Add comment..."
                    className="border p-1 w-full mt-2"
                  />

                  <button
                    onClick={() => handleComment(post.id)}
                    className="text-blue-500"
                  >
                    Comment
                  </button>
              </div>

              {visibleComments[post.id] && (
                <div>

                  {comments[post.id]?.map((c) => (
                    <p key={c.id} className="text-sm">
                      {c.content}
                    </p>
                  ))}

                </div>
              )}
            </div>
          </div>
        ))}

        {loading && <div className="text-center py-4">Loading...</div>}
      </div>
    </div>
  );
}
