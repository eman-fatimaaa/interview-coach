import axios from "axios";
import { getToken } from "./auth";

const apiBase = import.meta.env.VITE_API_BASE_URL || "http://localhost:8000";

export const api = axios.create({
  baseURL: apiBase,
});

api.interceptors.request.use((config) => {
  const t = getToken();
  if (t) config.headers.Authorization = `Bearer ${t}`;
  return config;
});

export function asError(e) {
  return e?.response?.data?.detail || e?.message || "Unknown error";
}
