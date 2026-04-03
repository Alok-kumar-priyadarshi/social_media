// This file extracts user id from JWT token

export function getUserIdFromToken() {
  const token = localStorage.getItem("token");

  if (!token) return null;

  const payload = JSON.parse(atob(token.split(".")[1]));
  return payload.user_id || payload.sub;
}