const BASE = "/api";

async function get(path) {
  const res = await fetch(`${BASE}${path}`);
  if (!res.ok) throw new Error(`${res.status} ${path}`);
  return res.json();
}

export const api = {
  health: () => get("/health"),
  summary: (days = 7) => get(`/summary?days=${days}`),
  topSkus: (days = 30, limit = 10) => get(`/top-skus?days=${days}&limit=${limit}`),
  orders: (days = 7) => get(`/orders?days=${days}`),
};
