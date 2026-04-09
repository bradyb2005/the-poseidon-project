// frontend/js/admin.js

function renderAdmin() {
  const root = document.getElementById("app-root");

  // Auth guard
  const user = JSON.parse(localStorage.getItem("user")) || "null";
  if (!user || !user.is_admin) {
    renderLogin();
    return;
  }

  if (user.role !== "admin") {
    renderHomepage();
    return;
  }

  root.innerHTML = `
    <div class="admin-wrapper">
      <div class="admin-header">
        <h1>🔱 Poseidon — Admin Panel</h1>
        <div>
          <span id="admin-name" style="color:#aac4ff; font-size:0.85rem; margin-right:1rem;">
            👤 ${user.username}
          </span>
          <a href="#" onclick="handleAdminLogout()">Log out</a>
        </div>
      </div>

      <div class="tabs">
        <button class="tab-btn active" id="tab-btn-dashboard" onclick="switchTab('dashboard', this)">📊 Dashboard</button>
        <button class="tab-btn" id="tab-btn-users" onclick="switchTab('users', this)">👥 Users</button>
        <button class="tab-btn" id="tab-btn-orders" onclick="switchTab('orders', this)">📦 Orders</button>
        <button class="tab-btn" id="tab-btn-analytics" onclick="switchTab('analytics', this)">📈 Analytics</button>
      </div>

      <!-- DASHBOARD TAB -->
      <div class="tab-content active" id="tab-dashboard">
        <div class="stats-grid" id="stats-grid">
          <div class="stat-card"><div class="stat-number">...</div><div class="stat-label">Loading</div></div>
        </div>
        <div class="card">
          <div class="section-title">🏆 Top Restaurants by Orders</div>
          <ul class="top-list" id="top-restaurants"><li>Loading...</li></ul>
        </div>
      </div>

      <!-- USERS TAB -->
      <div class="tab-content" id="tab-users">
        <div class="card">
          <div class="filters">
            <div class="filter-group">
              <label>Search</label>
              <input type="text" id="user-search" placeholder="username or email">
            </div>
            <div class="filter-group">
              <label>Role</label>
              <select id="user-role">
                <option value="">All</option>
                <option value="customer">Customer</option>
                <option value="owner">Owner</option>
                <option value="admin">Admin</option>
              </select>
            </div>
            <div class="filter-group">
              <label>Status</label>
              <select id="user-suspended">
                <option value="">All</option>
                <option value="false">Active</option>
                <option value="true">Suspended</option>
              </select>
            </div>
            <div class="filter-group">
              <label>Sort by</label>
              <select id="user-sort">
                <option value="username">Username</option>
                <option value="email">Email</option>
                <option value="id">ID</option>
              </select>
            </div>
            <div class="filter-group">
              <label>&nbsp;</label>
              <button onclick="loadUsers(1)">🔍 Search</button>
            </div>
          </div>
          <div class="table-wrap">
            <table>
              <thead>
                <tr>
                  <th>ID</th><th>Username</th><th>Email</th>
                  <th>Role</th><th>Status</th><th>Actions</th>
                </tr>
              </thead>
              <tbody id="users-tbody">
                <tr><td colspan="6" class="empty-state">Loading...</td></tr>
              </tbody>
            </table>
          </div>
          <div class="pagination" id="users-pagination"></div>
          <div class="action-msg" id="user-action-msg"></div>
        </div>
      </div>

      <!-- ORDERS TAB -->
      <div class="tab-content" id="tab-orders">
        <div class="card">
          <div class="filters">
            <div class="filter-group">
              <label>Customer ID</label>
              <input type="text" id="order-customer" placeholder="customer id">
            </div>
            <div class="filter-group">
              <label>Min Value ($)</label>
              <input type="number" id="order-min" placeholder="0">
            </div>
            <div class="filter-group">
              <label>Max Value ($)</label>
              <input type="number" id="order-max" placeholder="999">
            </div>
            <div class="filter-group">
              <label>Date From</label>
              <input type="date" id="order-date-from">
            </div>
            <div class="filter-group">
              <label>Date To</label>
              <input type="date" id="order-date-to">
            </div>
            <div class="filter-group">
              <label>Sort by</label>
              <select id="order-sort">
                <option value="order_time">Date</option>
                <option value="order_value">Value</option>
              </select>
            </div>
            <div class="filter-group">
              <label>&nbsp;</label>
              <button onclick="loadOrders(1)">🔍 Search</button>
            </div>
          </div>
          <div class="table-wrap">
            <table>
              <thead>
                <tr>
                  <th>Order ID</th><th>Customer ID</th><th>Item</th>
                  <th>Restaurant</th><th>Date</th><th>Value</th><th>Distance</th>
                </tr>
              </thead>
              <tbody id="orders-tbody">
                <tr><td colspan="7" class="empty-state">Loading...</td></tr>
              </tbody>
            </table>
          </div>
          <div class="pagination" id="orders-pagination"></div>
        </div>
      </div>

      <!-- ANALYTICS TAB -->
      <div class="tab-content" id="tab-analytics">
        <div class="stats-grid" id="analytics-stats">
          <div class="stat-card"><div class="stat-number">...</div><div class="stat-label">Loading</div></div>
        </div>
        <div style="display:grid; grid-template-columns: 1fr 1fr; gap:1rem;">
          <div class="card">
            <div class="section-title">📅 Orders by Month</div>
            <ul class="top-list" id="orders-by-month"><li>Loading...</li></ul>
          </div>
          <div class="card">
            <div class="section-title">🏆 Top Restaurants</div>
            <ul class="top-list" id="analytics-top-restaurants"><li>Loading...</li></ul>
          </div>
        </div>
      </div>
    </div>
  `;

  // Load dashboard by default
  loadDashboard();
}

// ── Tab switching ────────────────────────────────────────
function switchTab(name, btn) {
  document.querySelectorAll(".tab-content").forEach(t => t.classList.remove("active"));
  document.querySelectorAll(".tab-btn").forEach(b => b.classList.remove("active"));
  document.getElementById(`tab-${name}`).classList.add("active");
  btn.classList.add("active");

  if (name === "dashboard") loadDashboard();
  if (name === "users") loadUsers(1);
  if (name === "orders") loadOrders(1);
  if (name === "analytics") loadAnalytics();
}

// ── Dashboard ────────────────────────────────────────────
async function loadDashboard() {
  try {
    const res = await fetch(`${API_BASE}/admin/analytics`);
    const d = await res.json();

    document.getElementById("stats-grid").innerHTML = `
      <div class="stat-card">
        <div class="stat-number">${d.total_users}</div>
        <div class="stat-label">Total Users</div>
      </div>
      <div class="stat-card">
        <div class="stat-number">${d.suspended_users}</div>
        <div class="stat-label">Suspended</div>
      </div>
      <div class="stat-card">
        <div class="stat-number">${d.total_orders}</div>
        <div class="stat-label">Total Orders</div>
      </div>
      <div class="stat-card">
        <div class="stat-number">$${d.total_revenue.toLocaleString()}</div>
        <div class="stat-label">Total Revenue</div>
      </div>
      <div class="stat-card">
        <div class="stat-number">$${d.avg_order_value}</div>
        <div class="stat-label">Avg Order Value</div>
      </div>
      <div class="stat-card">
        <div class="stat-number">${d.total_notifications}</div>
        <div class="stat-label">Notifications</div>
      </div>
    `;

    document.getElementById("top-restaurants").innerHTML =
      d.top_restaurants.map((r, i) => `
        <li>
          <span>${i + 1}. Restaurant #${r.restaurant_id}</span>
          <span><strong>${r.order_count}</strong> orders</span>
        </li>
      `).join("") || "<li>No data</li>";

  } catch (err) {
    document.getElementById("stats-grid").innerHTML =
      '<div class="empty-state">⚠️ Could not load dashboard.</div>';
  }
}

// ── Users ────────────────────────────────────────────────
let currentUserPage = 1;

async function loadUsers(page) {
  currentUserPage = page;
  const search = document.getElementById("user-search").value.trim();
  const role = document.getElementById("user-role").value;
  const suspended = document.getElementById("user-suspended").value;
  const sortBy = document.getElementById("user-sort").value;

  let url = `${API_BASE}/admin/users?page=${page}&page_size=10&sort_by=${sortBy}`;
  if (search) url += `&search=${encodeURIComponent(search)}`;
  if (role) url += `&role=${role}`;
  if (suspended !== "") url += `&is_suspended=${suspended}`;

  try {
    const res = await fetch(url);
    const d = await res.json();
    const tbody = document.getElementById("users-tbody");

    if (!d.users || d.users.length === 0) {
      tbody.innerHTML = '<tr><td colspan="6" class="empty-state">No users found.</td></tr>';
      document.getElementById("users-pagination").innerHTML = "";
      return;
    }

    tbody.innerHTML = d.users.map(u => `
      <tr>
        <td>${u.id}</td>
        <td><strong>${u.username}</strong></td>
        <td>${u.email}</td>
        <td><span class="badge badge-${u.role || 'customer'}">${u.role || 'customer'}</span></td>
        <td>
          <span class="badge ${u.is_suspended ? 'badge-suspended' : 'badge-active'}">
            ${u.is_suspended ? 'Suspended' : 'Active'}
          </span>
        </td>
        <td style="display:flex; gap:0.4rem; flex-wrap:wrap;">
          ${u.is_suspended
            ? `<button class="btn-sm" onclick="unsuspendUser('${u.id}')">✅ Unsuspend</button>`
            : `<button class="btn-warn" onclick="suspendUser('${u.id}')">⛔ Suspend</button>`
          }
          <button class="btn-danger" onclick="deleteUser('${u.id}')">🗑 Delete</button>
        </td>
      </tr>
    `).join("");

    renderPagination("users-pagination", d.total_pages, page, loadUsers);

  } catch (err) {
    document.getElementById("users-tbody").innerHTML =
      '<tr><td colspan="6" class="empty-state">⚠️ Could not load users.</td></tr>';
  }
}

async function suspendUser(id) {
  if (!confirm("Suspend this user?")) return;
  await fetch(`${API_BASE}/admin/users/${id}/suspend`, { method: "POST" });
  showActionMsg("user-action-msg", "User suspended!");
  loadUsers(currentUserPage);
}

async function unsuspendUser(id) {
  await fetch(`${API_BASE}/admin/users/${id}/unsuspend`, { method: "POST" });
  showActionMsg("user-action-msg", "User unsuspended!");
  loadUsers(currentUserPage);
}

async function deleteUser(id) {
  if (!confirm("Permanently delete this user? This cannot be undone.")) return;
  await fetch(`${API_BASE}/admin/users/${id}`, { method: "DELETE" });
  showActionMsg("user-action-msg", "User deleted.");
  loadUsers(currentUserPage);
}

// ── Orders ───────────────────────────────────────────────
async function loadOrders(page) {
  const customerId = document.getElementById("order-customer").value.trim();
  const minVal = document.getElementById("order-min").value;
  const maxVal = document.getElementById("order-max").value;
  const dateFrom = document.getElementById("order-date-from").value;
  const dateTo = document.getElementById("order-date-to").value;
  const sortBy = document.getElementById("order-sort").value;

  let url = `${API_BASE}/admin/orders?page=${page}&page_size=15&sort_by=${sortBy}&sort_order=desc`;
  if (customerId) url += `&customer_id=${encodeURIComponent(customerId)}`;
  if (minVal) url += `&min_value=${minVal}`;
  if (maxVal) url += `&max_value=${maxVal}`;
  if (dateFrom) url += `&date_from=${dateFrom}`;
  if (dateTo) url += `&date_to=${dateTo}`;

  try {
    const res = await fetch(url);
    const d = await res.json();
    const tbody = document.getElementById("orders-tbody");

    if (!d.orders || d.orders.length === 0) {
      tbody.innerHTML = '<tr><td colspan="7" class="empty-state">No orders found.</td></tr>';
      document.getElementById("orders-pagination").innerHTML = "";
      return;
    }

    tbody.innerHTML = d.orders.map(o => `
      <tr>
        <td>${new Date(o.order_time).toLocaleString()}</td>
        <td style="font-size:0.8rem;">${o.customer_id}</td>
        <td>${o.item_name || "—"}</td>
        <td>#${o.restaurant_id}</td>
        <td>${o.order_time}</td>
        <td><strong>$${parseFloat(o.order_value).toFixed(2)}</strong></td>
        <td>${o.delivery_distance} km</td>
      </tr>
    `).join("");

    renderPagination("orders-pagination", d.total_pages, page, loadOrders);

  } catch (err) {
    document.getElementById("orders-tbody").innerHTML =
      '<tr><td colspan="7" class="empty-state">⚠️ Could not load orders.</td></tr>';
  }
}

// ── Analytics ────────────────────────────────────────────
async function loadAnalytics() {
  try {
    const res = await fetch(`${API_BASE}/admin/analytics`);
    const d = await res.json();

    document.getElementById("analytics-stats").innerHTML = `
      <div class="stat-card">
        <div class="stat-number">${d.total_orders.toLocaleString()}</div>
        <div class="stat-label">Total Orders</div>
      </div>
      <div class="stat-card">
        <div class="stat-number">$${d.total_revenue.toLocaleString()}</div>
        <div class="stat-label">Total Revenue</div>
      </div>
      <div class="stat-card">
        <div class="stat-number">$${d.avg_order_value}</div>
        <div class="stat-label">Avg Order Value</div>
      </div>
      <div class="stat-card">
        <div class="stat-number">${d.total_users}</div>
        <div class="stat-label">Total Users</div>
      </div>
    `;

    document.getElementById("orders-by-month").innerHTML =
      d.orders_by_month.slice(-12).reverse().map(m => `
        <li>
          <span>${new Date(2026, m.month - 1).toLocaleString('default', { month: 'long' })}</span>
          <strong>${m.count} orders</strong>
        </li>
      `).join("") || "<li>No data</li>";

    document.getElementById("analytics-top-restaurants").innerHTML =
      d.top_restaurants.map((r, i) => `
        <li>
          <span>${i + 1}. ${r.restaurant_name || 'Restaurant #' + r.restaurant_id}</span>   
          <strong>${r.order_count} orders</strong>
        </li>
      `).join("") || "<li>No data</li>";

  } catch (err) {
    document.getElementById("analytics-stats").innerHTML =
      '<div class="empty-state">⚠️ Could not load analytics.</div>';
  }
}

// ── Helpers ──────────────────────────────────────────────
function renderPagination(containerId, totalPages, currentPage, loadFn) {
  const container = document.getElementById(containerId);
  if (totalPages <= 1) { container.innerHTML = ""; return; }

  let html = "";
  if (currentPage > 3) {
    html += `<button onclick="${loadFn.name}(1)">1</button>`;
    if (currentPage > 4) html += `<span style="padding:0.4rem">...</span>`;
  }

  for (let i = Math.max(1, currentPage - 2); i <= Math.min(totalPages, currentPage + 2); i++) {
    html += `<button class="${i === currentPage ? 'active' : ''}"
      onclick="${loadFn.name}(${i})">${i}</button>`;
  }

  if (currentPage < totalPages - 2) {
    if (currentPage < totalPages - 3) html += `<span style="padding:0.4rem">...</span>`;
    html += `<button onclick="${loadFn.name}(${totalPages})">${totalPages}</button>`;
  }

  container.innerHTML = html;
}

function showActionMsg(id, text) {
  const el = document.getElementById(id);
  el.textContent = text;
  el.style.display = "block";
  setTimeout(() => el.style.display = "none", 3000);
}

function handleAdminLogout() {
  localStorage.removeItem("user");
  renderHomepage();
}
