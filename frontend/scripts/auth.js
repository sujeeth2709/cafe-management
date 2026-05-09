function saveSession(token, user) {
  // CHANGED: Use sessionStorage
  sessionStorage.setItem('token', token);
  sessionStorage.setItem('user', JSON.stringify(user));
}

function clearSession() {
  // CHANGED: Use sessionStorage
  sessionStorage.removeItem('token');
  sessionStorage.removeItem('user');
}

function getCurrentUser() {
  // CHANGED: Use sessionStorage
  const u = sessionStorage.getItem('user');
  return u ? JSON.parse(u) : null;
}

function isLoggedIn() {
  return !!getToken();
}

function getPathPrefix() {
  return window.location.pathname.includes('/admin/') ? '../' : '';
}

function requireAuth() {
  if (!isLoggedIn()) {
    window.location.href = getPathPrefix() + 'login.html';
  }
}

function requireAdmin() {
  const user = getCurrentUser();
  if (!user || user.role !== 'admin') {
    window.location.href = getPathPrefix() + 'login.html';
  }
}

function redirectIfLoggedIn() {
  if (isLoggedIn()) {
    window.location.href = getPathPrefix() + 'admin/index.html';
  }
}

function logout() {
  clearSession();
  window.location.href = getPathPrefix() + 'login.html';
}
