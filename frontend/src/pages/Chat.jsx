import { useEffect, useRef, useState, useCallback } from "react";
import API from "../api/axios";
import useChat from "../websocket/useChat";
import { getUserIdFromToken } from "../utils/auth";

export default function Chat() {
  const [inbox, setInbox] = useState([]);
  const [chatUsers, setChatUsers] = useState([]);
  const [selectedUser, setSelectedUser] = useState(null);
  const [messages, setMessages] = useState([]);
  const [text, setText] = useState("");
  const [typingUser, setTypingUser] = useState(null);

  const bottomRef = useRef();
  const selectedUserRef = useRef(null);
  const currentUserId = getUserIdFromToken();

  useEffect(() => {
    selectedUserRef.current = selectedUser;
  }, [selectedUser]);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  // ✅ SIMPLE NORMALIZER (DON’T OVERDO)
  const normalizeMessage = (msg) => ({
    ...msg,
    content: msg.content || msg.message,
    receiver_id:
      msg.receiver_id ||
      msg.to_user_id ||
      (msg.sender_id === currentUserId ? selectedUserRef.current?.id : currentUserId),
  });

  const loadInbox = async () => {
    const res = await API.get("/messages/inbox");
    setInbox(res.data);
  };

  const loadUsers = async () => {
    const res = await API.get("/messages/users");
    setChatUsers(res.data);
  };

  useEffect(() => {
    loadInbox();
    loadUsers();
  }, []);

  // ✅ FIXED HANDLER (CLEAN + SAFE)
  const handleIncomingMessage = useCallback((rawMsg) => {
    // 🔥 ALWAYS update inbox (independent)
    loadInbox();

    const activeUser = selectedUserRef.current;
    if (!activeUser) return;

    const msg = normalizeMessage(rawMsg);

    // typing
    if (rawMsg.type === "typing") {
      if (msg.sender_id === activeUser.id) {
        setTypingUser(msg.sender_id);
        setTimeout(() => setTypingUser(null), 1500);
      }
      return;
    }

    // seen
    if (rawMsg.type === "seen") {
      if (msg.sender_id === activeUser.id) {
        setMessages((prev) =>
          prev.map((m) =>
            m.sender_id === currentUserId ? { ...m, seen: true } : m
          )
        );
      }
      return;
    }

    // ✅ FILTER (SAFE)
    const isRelevant =
      (msg.sender_id === activeUser.id &&
        (msg.receiver_id === currentUserId || !msg.receiver_id)) ||
      (msg.sender_id === currentUserId &&
        msg.receiver_id === activeUser.id);

    if (!isRelevant) return;

    setMessages((prev) => [...prev, msg]);

  }, [currentUserId]);

  const { sendMessage } = useChat(handleIncomingMessage);

  const loadMessages = async (user) => {
    const res = await API.get(`/messages/${user.id}`);
    setMessages(res.data.map(normalizeMessage));
    setSelectedUser(user);

    sendMessage({
      type: "seen",
      to_user_id: user.id,
    });

    loadInbox();
  };

  const handleSend = () => {
    if (!text.trim() || !selectedUser) return;

    const tempMessage = normalizeMessage({
      sender_id: currentUserId,
      receiver_id: selectedUser.id,
      content: text,
      created_at: new Date().toISOString(),
    });

    setMessages((prev) => [...prev, tempMessage]);

    sendMessage({
      to_user_id: selectedUser.id,
      message: text,
    });

    setText("");
  };

  // merge users
  const mergedUsersMap = new Map();

  inbox.forEach((chat) => {
    mergedUsersMap.set(chat.user.id, {
      ...chat.user,
      last_message: chat.last_message,
      unread_count: chat.unread_count,
    });
  });

  chatUsers.forEach((user) => {
    if (!mergedUsersMap.has(user.id)) {
      mergedUsersMap.set(user.id, {
        ...user,
        last_message: null,
        unread_count: 0,
      });
    }
  });

  const mergedUsers = Array.from(mergedUsersMap.values());

  return (
    <div className="flex h-screen">
      {/* LEFT */}
      <div className="w-1/3 border-r overflow-y-auto bg-white">
        <h2 className="p-4 font-bold text-lg border-b">Chats</h2>

        {mergedUsers.map((user) => (
          <div
            key={user.id}
            onClick={() => loadMessages(user)}
            className={`p-4 border-b cursor-pointer hover:bg-gray-100 ${
              selectedUser?.id === user.id ? "bg-gray-200" : ""
            }`}
          >
            <p className="font-semibold">{user.username}</p>
            <p className="text-sm text-gray-500 truncate">
              {user.last_message || "Start conversation"}
            </p>

            {user.unread_count > 0 && (
              <span className="bg-red-500 text-white px-2 py-1 rounded-full text-xs">
                {user.unread_count}
              </span>
            )}
          </div>
        ))}
      </div>

      {/* RIGHT */}
      <div className="w-2/3 flex flex-col">
        <div className="p-4 border-b bg-white">
          {selectedUser ? (
            <>
              <p className="font-semibold text-lg">
                {selectedUser.username}
              </p>
              {typingUser === selectedUser.id && (
                <p className="text-xs text-gray-500">Typing...</p>
              )}
            </>
          ) : (
            <p className="text-gray-500">Select a chat</p>
          )}
        </div>

        <div className="flex-1 p-4 overflow-y-auto bg-gray-50">
          {messages.map((m) => {
            const isMine = m.sender_id === currentUserId;

            return (
              <div
                key={m.id || `${m.sender_id}-${m.created_at}`}
                className={`flex ${
                  isMine ? "justify-end" : "justify-start"
                } mb-2`}
              >
                <div
                  className={`px-4 py-2 rounded-2xl max-w-xs shadow ${
                    isMine
                      ? "bg-blue-500 text-white"
                      : "bg-white border"
                  }`}
                >
                  <p>{m.content}</p>

                  <div className="text-xs mt-1 opacity-70">
                    {m.created_at &&
                      new Date(m.created_at).toLocaleTimeString()}
                  </div>

                  {isMine && m.seen && (
                    <p className="text-xs mt-1 opacity-70">Seen</p>
                  )}
                </div>
              </div>
            );
          })}
          <div ref={bottomRef}></div>
        </div>

        {selectedUser && (
          <div className="p-3 border-t flex gap-2 bg-white">
            <input
              value={text}
              onChange={(e) => {
                setText(e.target.value);

                sendMessage({
                  type: "typing",
                  to_user_id: selectedUser.id,
                });
              }}
              onKeyDown={(e) => {
                if (e.key === "Enter") handleSend();
              }}
              placeholder="Type a message..."
              className="flex-1 border p-2 rounded"
            />

            <button
              onClick={handleSend}
              className="bg-blue-500 text-white px-4 rounded"
            >
              Send
            </button>
          </div>
        )}
      </div>
    </div>
  );
}