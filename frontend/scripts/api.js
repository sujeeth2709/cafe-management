const BASE_URL = ''; // Same domain — works both locally and on Render

function getToken() {
  return localStorage.getItem('token');
}

async function apiFetch(path, options = {}) {
  const token = getToken();
  const headers = { 'Content-Type': 'application/json', ...options.headers };
  if (token) headers['Authorization'] = `Bearer ${token}`;

  const res = await fetch(`${BASE_URL}${path}`, { ...options, headers });
  if (!res.ok) {
    const err = await res.json().catch(() => ({ detail: 'Unknown error' }));
    throw new Error(err.detail || res.statusText);
  }
  return res.json();
}

// ── Auth ──────────────────────────────────────────────
const Auth = {
  register: (name, email, password) =>
    apiFetch('/api/auth/register', { method: 'POST', body: JSON.stringify({ name, email, password }) }),
  login: (email, password) =>
    apiFetch('/api/auth/login', { method: 'POST', body: JSON.stringify({ email, password }) }),
};

// ── Menu ─────────────────────────────────────────────
const Menu = {
  getAll: () => apiFetch('/api/menu/'),
  getOne: (id) => apiFetch(`/api/menu/${id}`),
  create: (data) => apiFetch('/api/menu/', { method: 'POST', body: JSON.stringify(data) }),
  update: (id, data) => apiFetch(`/api/menu/${id}`, { method: 'PUT', body: JSON.stringify(data) }),
  delete: (id) => apiFetch(`/api/menu/${id}`, { method: 'DELETE' }),
};

// ── Cart ─────────────────────────────────────────────
const Cart = {
  validate: (itemIds) =>
    apiFetch('/api/cart/validate', { method: 'POST', body: JSON.stringify(itemIds) }),
};

// ── Orders ───────────────────────────────────────────
const Orders = {
  create: (items, tableNumber) =>
    apiFetch('/api/orders/', { method: 'POST', body: JSON.stringify({ items, table_number: tableNumber }) }),
  myOrders: () => apiFetch('/api/orders/me'),
  allOrders: () => apiFetch('/api/orders/'),
  updateStatus: (id, status) =>
    apiFetch(`/api/orders/${id}/status`, { method: 'PUT', body: JSON.stringify({ status }) }),
};

// ── Reservations ─────────────────────────────────────
const Reservations = {
  create: (date, time, guests, tableNumber) =>
    apiFetch('/api/reservations/', { method: 'POST', body: JSON.stringify({ date, time, guests, table_number: tableNumber }) }),
  myReservations: () => apiFetch('/api/reservations/me'),
  allReservations: () => apiFetch('/api/reservations/'),
  updateStatus: (id, status) =>
    apiFetch(`/api/reservations/${id}/status`, { method: 'PUT', body: JSON.stringify({ status }) }),
};

// ── Admin ────────────────────────────────────────────
const Admin = {
  dashboard: () => apiFetch('/api/admin/dashboard'),
  cashflow: () => apiFetch('/api/admin/cashflow'),
};
