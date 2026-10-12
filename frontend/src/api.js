const API_URL = import.meta.env.VITE_API_URL || "http://127.0.0.1:8000";
const REQUEST_TIMEOUT_MS = 90000;

export class ApiError extends Error {
  constructor(message, status) {
    super(message);
    this.status = status;
  }
}

function extractMessage(data, status) {
  const detail = data && data.detail;

  if (typeof detail === "string") {
    return detail;
  }
  if (Array.isArray(detail) && detail.length > 0) {
    const first = detail[0];
    const field = Array.isArray(first.loc) ? first.loc[first.loc.length - 1] : "input";
    return `${field}: ${first.msg.replace(/^Value error, /, "")}`;
  }
  return `Something went wrong (error ${status}).`;
}

async function request(path, { method = "GET", body, token } = {}) {
  const headers = { "Content-Type": "application/json" };
  if (token) {
    headers.Authorization = `Bearer ${token}`;
  }

  const controller = new AbortController();
  const timer = setTimeout(() => controller.abort(), REQUEST_TIMEOUT_MS);

  let response;
  try {
    response = await fetch(`${API_URL}${path}`, {
      method,
      headers,
      body: body ? JSON.stringify(body) : undefined,
      signal: controller.signal,
    });
  } catch (error) {
    if (error.name === "AbortError") {
      throw new ApiError("The request took too long. Please try again.", 0);
    }
    throw new ApiError("Cannot reach the server. Please check that the backend is running.", 0);
  } finally {
    clearTimeout(timer);
  }

  let data = null;
  try {
    data = await response.json();
  } catch {
    data = null;
  }

  if (!response.ok) {
    throw new ApiError(extractMessage(data, response.status), response.status);
  }
  return data;
}

export function signup(name, email, password) {
  return request("/signup", { method: "POST", body: { name, email, password } });
}

export function login(email, password) {
  return request("/login", { method: "POST", body: { email, password } });
}

export function sendChatMessage(message, token) {
  return request("/chatbot", { method: "POST", body: { message }, token });
}