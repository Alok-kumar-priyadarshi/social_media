import { useEffect, useRef } from "react";

export default function useChat(onMessage) {
  const ws = useRef(null);
  const reconnectTimeout = useRef(null);
  const messageQueue = useRef([]);
  const isConnecting = useRef(false);

  const connect = () => {
    const token = localStorage.getItem("token");
    const WS_URL = import.meta.env.VITE_WS_URL;

    // 🔒 Safety checks
    if (!token) {
      console.error("❌ No token found, WS not connecting");
      return;
    }

    if (!WS_URL) {
      console.error("❌ VITE_WS_URL not defined");
      return;
    }

    // 🚫 Prevent duplicate connections
    if (
      ws.current &&
      (ws.current.readyState === WebSocket.OPEN ||
        ws.current.readyState === WebSocket.CONNECTING)
    ) {
      return;
    }

    if (isConnecting.current) return;
    isConnecting.current = true;

    console.log("🔌 Connecting to:", `${WS_URL}/ws`);

    const socket = new WebSocket(`${WS_URL}/ws?token=${token}`);
    ws.current = socket;

    socket.onopen = () => {
      console.log("✅ WS Connected");
      isConnecting.current = false;

      // 🔥 Flush queued messages
      while (messageQueue.current.length > 0) {
        socket.send(messageQueue.current.shift());
      }
    };

    socket.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data);
        onMessage(data);
      } catch (err) {
        console.error("❌ WS Parse Error:", err);
      }
    };

    socket.onerror = (err) => {
      console.error("❌ WS Error:", err);
    };

    socket.onclose = () => {
      console.warn("⚠️ WS Disconnected");

      isConnecting.current = false;

      // 🔁 Controlled reconnect (avoid stacking)
      if (!reconnectTimeout.current) {
        reconnectTimeout.current = setTimeout(() => {
          reconnectTimeout.current = null;
          connect();
        }, 3000);
      }
    };
  };

  useEffect(() => {
    connect();

    // ❤️ Heartbeat (keeps connection alive on Render)
    const interval = setInterval(() => {
      if (ws.current?.readyState === WebSocket.OPEN) {
        ws.current.send(JSON.stringify({ type: "ping" }));
      }
    }, 30000);

    return () => {
      clearInterval(interval);
      clearTimeout(reconnectTimeout.current);

      if (ws.current) {
        ws.current.close();
      }
    };
  }, []);

  // 📤 Safe send function
  const sendMessage = (data) => {
    const message = JSON.stringify(data);

    if (ws.current?.readyState === WebSocket.OPEN) {
      ws.current.send(message);
    } else {
      console.warn("⚠️ WS not ready, queueing message...");
      messageQueue.current.push(message);
    }
  };

  return { sendMessage };
}