function saveSession(token, user) {
  localStorage.setItem('token', token);
  localStorage.setItem('user', JSON.stringify(user));
}

function clearSession() {
  localStorage.removeItem('token');
  localStorage.removeItem('user');
}

function getCurrentUser() {
  const u = localStorage.getItem('user');
  return u ? JSON.parse(u) : null;
}

function isLoggedIn() {
  return !!getToken();
}

function requireAuth() {
  if (!isLoggedIn()) {
    window.location.href = '/pages/login.html';
  }
}

function requireAdmin() {
  const user = getCurrentUser();
  if (!user || user.role !== 'admin') {
    window.location.href = '/pages/login.html';
  }
}

function redirectIfLoggedIn() {
  if (isLoggedIn()) {
    window.location.href = '/pages/admin/index.html';
  }
}

function logout() {
  clearSession();
  window.location.href = '/pages/login.html';
}
