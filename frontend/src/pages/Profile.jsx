// This page shows user profile (self + others) with proper UX, image, bio, and follow system

import { useEffect, useState } from "react";
import { useParams, useNavigate } from "react-router-dom";
import API from "../api/axios";
import Navbar from "../components/Navbar";
import FollowModal from "../components/FollowModal";

export default function Profile() {
  const { userId } = useParams();
  const navigate = useNavigate();

  const [user, setUser] = useState(null);
  const [posts, setPosts] = useState([]);
  const [isFollowing, setIsFollowing] = useState(false);
  const [myId, setMyId] = useState(null);
  const [modalType, setModalType] = useState(null);
  const [isBlocked, setIsBlocked] = useState(false);

  useEffect(() => {
    const loadProfile = async () => {
      try {
        // 🔹 Step 1: Get current user
        const meRes = await API.get("/users/me");
        const myUserId = meRes.data.id;
        setMyId(myUserId);

        const targetId = userId || myUserId;

        // 🔹 Step 2: Get profile
        if (userId) {
          const profileRes = await API.get(`/profile/${targetId}`);
          setUser({
            ...profileRes.data,
            profile_picture: profileRes.data.profile_image,
          });
        } else {
          setUser({
            ...meRes.data,
            profile_picture: meRes.data.profile_image,
          });
        }

        // console.log(profileRes)

        console.log("PROFILE DATA:", user);

        // 🔹 Step 3: Get posts
        const postsRes = await API.get(`/users/${targetId}/posts`);
        setPosts(postsRes.data);

        // 🔹 Step 4: Follow status
        if (userId && parseInt(userId) !== myUserId) {
          const followRes = await API.get(
            `/following/${myUserId}?offset=0&limit=1000`,
          );

          setIsFollowing(
            followRes.data.some((u) => u.id === parseInt(targetId)),
          );
        }
      } catch (err) {
        console.error("Profile error:", err);
      }

      if (userId && parseInt(userId) !== myUserId) {
        try {
          const blockRes = await API.get("/block/block");
          setIsBlocked(
            blockRes.data.some(
              (blockedUser) => blockedUser.id === parseInt(targetId),
            ),
          );
        } catch (err) {
          console.error("Block status error:", err);
        }
      }
    };

    loadProfile();
  }, [userId]);

  const handleBlock = async () => {
    if (!userId) return;

    const confirm = window.confirm(
      isBlocked ? "Unblock this user?" : "Block this user?",
    );

    if (!confirm) return;

    try {
      if (isBlocked) {
        await API.delete(`/block/${userId}`);
        setIsBlocked(false);
      } else {
        await API.post(`/block/${userId}`);
        setIsBlocked(true);
      }
    } catch (err) {
      console.error("Block error:", err);
    }
  };

  const handleFollow = async () => {
    if (!userId) return;

    try {
      if (isFollowing) {
        await API.delete(`/follow/${userId}`);
        setIsFollowing(false);
      } else {
        await API.post(`/follow/${userId}`);
        setIsFollowing(true);
      }
    } catch (err) {
      console.error("Follow error:", err);
    }
  };

  if (!user) return <div className="p-4">Loading profile...</div>;

  return (
    <div>
      {/* <Navbar /> */}

      <div className="max-w-3xl mx-auto p-4">
        {/* 🔥 PROFILE HEADER */}
        <div className="flex items-center gap-6 mb-6">
          {/* Profile Image */}
          <img
            src={
              user?.profile_image ||
              user?.profile_picture ||
              "/assets/image.png"
            }
            onError={(e) => {
              e.target.src = "/assets/image.png";
            }}
            alt="profile"
            className="w-20 h-20 rounded-full object-cover"
          />

          <div>
            {/* Username */}
            <h2 className="text-xl font-bold">{user.username}</h2>

            {/* Bio */}
            {user.bio && <p className="text-gray-600 mt-1">{user.bio}</p>}

            {/* Stats */}
            <div className="flex gap-4 mt-2">
              <span>
                <b>{posts.length}</b> posts
              </span>

              <span
                onClick={() => setModalType("followers")}
                className="cursor-pointer"
              >
                <b>{user.followers_count}</b> followers
              </span>

              <span
                onClick={() => setModalType("following")}
                className="cursor-pointer"
              >
                <b>{user.following_count}</b> following
              </span>
            </div>

            {/* 🔥 ACTION BUTTONS */}
            <div className="mt-3 flex gap-2">
              {/* Follow Button */}
              {userId && parseInt(userId) !== myId && (
                <button
                  onClick={handleFollow}
                  className={`px-4 py-1 rounded ${
                    isFollowing ? "bg-gray-300" : "bg-blue-500 text-white"
                  }`}
                >
                  {isFollowing ? "Unfollow" : "Follow"}
                </button>
              )}

              {/* Edit Profile (only self) */}
              {!userId && (
                <button
                  onClick={() => navigate("/edit-profile")}
                  className="px-4 py-1 rounded bg-gray-200"
                >
                  Edit Profile
                </button>
              )}
              {userId && parseInt(userId) !== myId && (
                <button
                  onClick={handleBlock}
                  className={`px-4 py-1 rounded ${
                    isBlocked ? "bg-gray-300" : "bg-red-500 text-white"
                  }`}
                >
                  {isBlocked ? "Unblock" : "Block"}
                </button>
              )}
            </div>
          </div>
        </div>

        {/* 🔥 POSTS GRID */}
        <div className="grid grid-cols-3 gap-2">
          {posts.map((post) => (
            <img
              key={post.id}
              src={post.image_url}
              className="w-full h-32 object-cover rounded"
            />
          ))}
        </div>
      </div>

      {/* 🔥 FOLLOWERS / FOLLOWING MODAL */}
      {modalType && (
        <FollowModal
          type={modalType}
          userId={userId || myId}
          onClose={() => setModalType(null)}
        />
      )}
    </div>
  );
}
