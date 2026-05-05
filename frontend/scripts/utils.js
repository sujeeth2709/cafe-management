// ── Toast ─────────────────────────────────────────────
function showToast(message, type = 'success') {
  const container = document.getElementById('toast-container') || createToastContainer();
  const toast = document.createElement('div');
  toast.className = `toast toast-${type}`;
  toast.textContent = message;
  container.appendChild(toast);
  setTimeout(() => toast.classList.add('show'), 10);
  setTimeout(() => {
    toast.classList.remove('show');
    setTimeout(() => toast.remove(), 300);
  }, 3000);
}

function createToastContainer() {
  const div = document.createElement('div');
  div.id = 'toast-container';
  document.body.appendChild(div);
  return div;
}

// ── Cart (localStorage) ───────────────────────────────
const CartStore = {
  get() {
    return JSON.parse(localStorage.getItem('cart') || '[]');
  },
  save(cart) {
    localStorage.setItem('cart', JSON.stringify(cart));
    updateCartBadge();
  },
  add(item) {
    const cart = this.get();
    const existing = cart.find(i => i.id === item.id);
    if (existing) {
      existing.qty += 1;
    } else {
      cart.push({ ...item, qty: 1 });
    }
    this.save(cart);
  },
  remove(itemId) {
    this.save(this.get().filter(i => i.id !== itemId));
  },
  updateQty(itemId, qty) {
    const cart = this.get();
    const item = cart.find(i => i.id === itemId);
    if (item) {
      item.qty = qty;
      if (item.qty <= 0) return this.remove(itemId);
    }
    this.save(cart);
  },
  clear() {
    this.save([]);
  },
  total() {
    return this.get().reduce((sum, i) => sum + i.price * i.qty, 0);
  },
  count() {
    return this.get().reduce((sum, i) => sum + i.qty, 0);
  }
};

function updateCartBadge() {
  const badge = document.getElementById('cart-badge');
  if (badge) {
    const count = CartStore.count();
    badge.textContent = count;
    badge.style.display = count > 0 ? 'inline-flex' : 'none';
  }
}

// ── Formatters ────────────────────────────────────────
function formatCurrency(amount) {
  return '₹' + Number(amount).toFixed(2);
}

function formatDate(dateStr) {
  return new Date(dateStr).toLocaleDateString('en-IN', {
    day: '2-digit', month: 'short', year: 'numeric'
  });
}

function formatDateTime(dtStr) {
  return new Date(dtStr).toLocaleString('en-IN', {
    day: '2-digit', month: 'short', year: 'numeric',
    hour: '2-digit', minute: '2-digit'
  });
}

function statusBadge(status) {
  const colors = {
    pending: '#f59e0b',
    confirmed: '#3b82f6',
    preparing: '#8b5cf6',
    delivered: '#10b981',
    cancelled: '#ef4444',
  };
  const color = colors[status] || '#6b7280';
  return `<span class="status-badge" style="background:${color}20;color:${color};border:1px solid ${color}40">${status}</span>`;
}
