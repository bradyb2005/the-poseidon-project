// frontend/js/delivery.js

function renderDeliveryPage() {
  const root = document.getElementById("app-root");

  root.innerHTML = `
    <div class="page-card">
      <div class="page-header">
        <h2>🚚 Delivery Dashboard</h2>
        <a href="#" onclick="renderHomepage()">Home</a>
      </div>

      <div class="section">
        <h3>Create Delivery</h3>

        <div class="form-group">
          <label for="delivery_id">Delivery ID</label>
          <input id="delivery_id" type="number" placeholder="Enter delivery ID">
        </div>

        <div class="form-group">
          <label for="order_id">Order ID</label>
          <input id="order_id" type="number" placeholder="Enter order ID">
        </div>

        <div class="form-group">
          <label for="status">Status</label>
          <select id="status">
            <option value="pending">pending</option>
            <option value="assigned">assigned</option>
            <option value="picked_up">picked_up</option>
            <option value="on_the_way">on_the_way</option>
            <option value="delivered">delivered</option>
          </select>
        </div>

        <div class="form-group">
          <label for="eta">Estimated Arrival</label>
          <input id="eta" type="text" placeholder="Optional ETA">
        </div>

        <div class="form-group">
          <label for="driver_name">Driver Name</label>
          <input id="driver_name" type="text" placeholder="Optional driver name">
        </div>

        <div class="form-group">
          <label for="driver_contact">Driver Contact</label>
          <input id="driver_contact" type="text" placeholder="Optional driver contact">
        </div>

        <button onclick="createDelivery()">Create</button>
        <div class="message" id="create-message" style="display: none;"></div>
      </div>

      <div class="section">
        <h3>All Deliveries</h3>
        <button onclick="loadDeliveries()">🔄 Refresh</button>
        <div id="delivery-list" style="margin-top: 1rem;"></div>
      </div>
    </div>
  `;

  loadDeliveries();
}

function showMessage(el, text, type) {
  el.textContent = text;
  el.className = `message ${type}`;
  el.style.display = "block";
}

async function createDelivery() {
  const messageBox = document.getElementById("create-message");

  const deliveryId = parseInt(document.getElementById("delivery_id").value);
  const orderId = parseInt(document.getElementById("order_id").value);
  const status = document.getElementById("status").value;
  const eta = document.getElementById("eta").value.trim();
  const driverName = document.getElementById("driver_name").value.trim();
  const driverContact = document.getElementById("driver_contact").value.trim();

  if (isNaN(deliveryId) || isNaN(orderId) || deliveryId <= 0 || orderId <= 0) {
    showMessage(messageBox, "Enter valid positive delivery and order IDs.", "error");
    return;
  }

  const data = {
    delivery_id: deliveryId,
    order_id: orderId,
    status: status,
    estimated_arrival: eta || null,
    driver_name: driverName || null,
    driver_contact: driverContact || null
  };

  try {
    const response = await fetch(`${API_BASE}/deliveries/`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(data)
    });

    const result = await response.json();

    if (!response.ok) {
      showMessage(messageBox, result.detail || "Error creating delivery.", "error");
      return;
    }

    showMessage(messageBox, "Delivery created successfully!", "success");

    document.getElementById("delivery_id").value = "";
    document.getElementById("order_id").value = "";
    document.getElementById("status").value = "pending";
    document.getElementById("eta").value = "";
    document.getElementById("driver_name").value = "";
    document.getElementById("driver_contact").value = "";

    loadDeliveries();
  } catch (err) {
    showMessage(messageBox, "Cannot reach server. Is the backend running?", "error");
  }
}

async function loadDeliveries() {
  const container = document.getElementById("delivery-list");
  if (!container) return;

  container.innerHTML = "<p>Loading deliveries...</p>";

  try {
    const response = await fetch(`${API_BASE}/deliveries/`);
    const deliveries = await response.json();

    if (!response.ok) {
      container.innerHTML = `<p>${deliveries.detail || "Failed to load deliveries."}</p>`;
      return;
    }

    if (!deliveries.length) {
      container.innerHTML = `<div class="empty-state">No deliveries yet.</div>`;
      return;
    }

    container.innerHTML = deliveries.map(d => `
      <div class="delivery-card">
        <div><strong>Delivery ID:</strong> ${d.delivery_id}</div>
        <div><strong>Order ID:</strong> ${d.order_id}</div>
        <div><strong>Status:</strong> ${d.status}</div>
        <div><strong>ETA:</strong> ${d.estimated_arrival || "N/A"}</div>
        <div><strong>Driver:</strong> ${d.driver_name || "N/A"}</div>
        <div><strong>Contact:</strong> ${d.driver_contact || "N/A"}</div>

        <div class="form-group" style="margin-top: 0.8rem;">
          <label for="status-${d.delivery_id}">Update Status</label>
          <select id="status-${d.delivery_id}">
            <option value="pending" ${d.status === "pending" ? "selected" : ""}>pending</option>
            <option value="assigned" ${d.status === "assigned" ? "selected" : ""}>assigned</option>
            <option value="picked_up" ${d.status === "picked_up" ? "selected" : ""}>picked_up</option>
            <option value="on_the_way" ${d.status === "on_the_way" ? "selected" : ""}>on_the_way</option>
            <option value="delivered" ${d.status === "delivered" ? "selected" : ""}>delivered</option>
          </select>
        </div>

        <div class="actions">
          <button onclick="updateStatus(${d.delivery_id})">Update Status</button>
          <button onclick="deleteDelivery(${d.delivery_id})">Delete</button>
        </div>
      </div>
    `).join("");
  } catch (err) {
    container.innerHTML = "<p>Error loading deliveries.</p>";
  }
}

async function updateStatus(deliveryId) {
  const newStatus = document.getElementById(`status-${deliveryId}`).value;

  try {
    const response = await fetch(`${API_BASE}/deliveries/${deliveryId}/status`, {
      method: "PUT",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        status: newStatus,
        estimated_arrival: null
      })
    });

    const result = await response.json();

    if (!response.ok) {
      alert(result.detail || "Failed to update status.");
      return;
    }

    loadDeliveries();
  } catch (err) {
    alert("Failed to update status.");
  }
}

async function deleteDelivery(deliveryId) {
  try {
    const response = await fetch(`${API_BASE}/deliveries/${deliveryId}`, {
      method: "DELETE"
    });

    const result = await response.json();

    if (!response.ok) {
      alert(result.detail || "Delete failed.");
      return;
    }

    loadDeliveries();
  } catch (err) {
    alert("Delete failed.");
  }
}