import { useEffect, useRef } from "react";

export default function useChat(onMessage) {
  const ws = useRef(null);
  const reconnectTimeout = useRef(null);
  const messageQueue = useRef([]);

  const connect = () => {
    const token = localStorage.getItem("token");

    ws.current = new WebSocket(`ws://127.0.0.1:8000/ws?token=${token}`);

    ws.current.onopen = () => {
      console.log("✅ WS Connected");

      // 🔥 flush queued messages
      while (messageQueue.current.length > 0) {
        ws.current.send(messageQueue.current.shift());
      }
    };

    ws.current.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data);
        onMessage(data);
      } catch (err) {
        console.error("WS Parse Error:", err);
      }
    };

    ws.current.onerror = (err) => {
      console.error("❌ WS Error:", err);
    };

    ws.current.onclose = () => {
      console.log("⚠️ WS Disconnected. Reconnecting...");

      // 🔥 auto reconnect
      reconnectTimeout.current = setTimeout(() => {
        connect();
      }, 2000);
    };
  };

  useEffect(() => {
    connect();

    // 🔥 heartbeat (keep connection alive)
    const interval = setInterval(() => {
      if (ws.current?.readyState === WebSocket.OPEN) {
        ws.current.send(JSON.stringify({ type: "ping" }));
      }
    }, 30000);

    return () => {
      clearInterval(interval);
      clearTimeout(reconnectTimeout.current);
      ws.current?.close();
    };
  }, []);

  // 🔥 SAFE SEND
  const sendMessage = (data) => {
    const message = JSON.stringify(data);

    if (ws.current?.readyState === WebSocket.OPEN) {
      ws.current.send(message);
    } else {
      console.warn("WS not ready, queueing message...");
      messageQueue.current.push(message);
    }
  };

  return { sendMessage };
}