// This file defines all routes

import { BrowserRouter, Routes, Route } from "react-router-dom";

import Login from "./pages/Login";
import Signup from "./pages/Signup";
import Feed from "./pages/Feed";
import Chat from "./pages/Chat";
import Profile from "./pages/Profile";
import CreatePost from "./pages/CreatePost";
import EditProfile from "./pages/EditProfile";
import Layout from "./components/Layout";
import Settings from "./pages/Settings";


function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Layout><Feed /></Layout>} />
        <Route path="/login" element={<Login />} />
        <Route path="/signup" element={<Signup />} />
        <Route path="/chat" element={<Layout><Chat /></Layout>} />
        <Route path="/profile" element={<Layout><Profile /></Layout>} />
        <Route path="/profile/:userId" element={<Layout><Profile /></Layout>} />
        <Route path="/create" element={<Layout><CreatePost /></Layout>} />
        <Route path="/edit-profile" element={<Layout><EditProfile /></Layout>} />
        <Route path="/settings" element={<Layout><Settings /></Layout>} />
        
      </Routes>
    </BrowserRouter>
  );
}

export default App;