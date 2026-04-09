// frontend/js/notifications.js

function renderNotifications() {
  const root = document.getElementById("app-root");

  // Check if user is logged in
  const user = JSON.parse(localStorage.getItem("user") || "null");

  if (!user) {
    renderLogin();
    return;
  }

  root.innerHTML = `
    <div class="page-card">
      <div class="page-header">
        <h1>🔱 Poseidon</h1>
        <div class="nav-links">
          <span class="user-info">👤 ${user.username}</span>
          <a href="#" onclick="handleLogout()">Log out</a>
        </div>
      </div>

      <div class="toolbar">
        <button onclick="loadNotifications()">🔄 Refresh</button>
        <button class="btn-secondary" onclick="renderHomepage()">← Back to Home</button>
      </div>

      <div class="notifications-list" id="notifications-list">
        <div class="loading">Loading notifications...</div>
      </div>
    </div>
  `;

  // Load notifications right away
  loadNotifications();
}

async function loadNotifications() {
  const user = JSON.parse(localStorage.getItem("user") || "null");
  const list = document.getElementById("notifications-list");

  list.innerHTML = '<div class="loading">Loading...</div>';

  try {
    const response = await fetch(`${API_BASE}/notifications/${user.id}`);
    const data = await response.json();

    const notifications = data.notifications || [];

    if (notifications.length === 0) {
      list.innerHTML = `
        <div class="empty-state">
          <div class="icon">🔔</div>
          <p>No notifications yet!</p>
          <p style="font-size:0.85rem; margin-top:0.5rem;">
            Notifications will appear here when orders are placed,
            payments are made, or reviews are flagged.
          </p>
        </div>`;
      return;
    }

    // Sort: unread first, then by id descending
    notifications.sort((a, b) => {
      if (a.is_read !== b.is_read) return a.is_read ? 1 : -1;
      return parseInt(b.id) - parseInt(a.id);
    });

    list.innerHTML = notifications.map(n => `
    <div class="notif-item ${n.is_read ? 'read' : 'unread'} ${!n.enabled ? 'disabled' : ''}">
        <div>
            ${!n.is_read ? `<button onclick="markAsRead(${n.id})">Mark as read</button>` : ''}
            <div class="notif-message">${n.message}</div>
          <div class="notif-type">
            Type: ${n.type}
            ${!n.enabled ? '· <span style="color:#e55">disabled</span>' : ''}
          </div>
        </div>
        <span class="notif-badge ${n.is_read ? 'read' : ''}">
          ${n.is_read ? 'read' : 'new'}
        </span>
      </div>
    `).join("");

  } catch (err) {
    list.innerHTML = `
      <div class="empty-state">
        <div class="icon">⚠️</div>
        <p>Could not load notifications.</p>
        <p style="font-size:0.85rem;">Is the backend running?</p>
      </div>`;
  }
}

function handleLogout() {
  localStorage.removeItem("user");
  renderHomepage();
}

async function markAsRead(notificationId) {
    try {
        await fetch(`${API_BASE}/notifications/${notificationId}/read`, {
            method: "PATCH",
            headers: { "Content-Type": "application/json" }
        });
        loadNotifications();
    } catch (err) {
        console.error("Could not mark notification as read.", err);
    }
}
