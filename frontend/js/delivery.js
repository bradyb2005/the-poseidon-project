let deliveriesCache = {};

function renderDeliveryPage() {
  const root = document.getElementById("app-root");

  root.innerHTML = `
    <div class="page-card">
      <h2>🚚 Delivery Dashboard</h2>

      <div class="section">
        <h3>Create Delivery</h3>

        <input id="order_id" placeholder="Order ID" type="number" />
        <input id="eta" placeholder="ETA (optional)" />
        <input id="driver_name" placeholder="Driver name (optional)" />
        <input id="driver_contact" placeholder="Driver contact (optional)" />

        <select id="status">
          <option value="pending">pending</option>
          <option value="assigned">assigned</option>
          <option value="picked_up">picked_up</option>
          <option value="on_the_way">on_the_way</option>
          <option value="delivered">delivered</option>
        </select>

        <button onclick="createDelivery()">Create</button>
        <div id="create-msg"></div>
      </div>

      <div class="section">
        <h3>All Deliveries</h3>
        <button onclick="loadDeliveries()">Refresh</button>
        <div id="delivery-list"></div>
      </div>
    </div>
  `;

  loadDeliveries();
}

function showMsg(el, text) {
  el.innerText = text;
}

async function createDelivery() {
  const msg = document.getElementById("create-msg");

  const order_id = parseInt(document.getElementById("order_id").value);
  const status = document.getElementById("status").value;
  const eta = document.getElementById("eta").value;
  const driver_name = document.getElementById("driver_name").value;
  const driver_contact = document.getElementById("driver_contact").value;

  if (!order_id || order_id <= 0) {
    showMsg(msg, "Invalid order ID");
    return;
  }

  const payload = {
    order_id,
    status,
    estimated_arrival: eta || null,
    driver_name: driver_name || null,
    driver_contact: driver_contact || null
  };

  try {
    const res = await fetch(`${API_BASE}/deliveries/`, {
      method: "POST",
      headers: {"Content-Type": "application/json"},
      body: JSON.stringify(payload)
    });

    const data = await res.json();

    if (!res.ok) {
      showMsg(msg, data.detail || "Error");
      return;
    }

    showMsg(msg, "Created!");
    loadDeliveries();

  } catch {
    showMsg(msg, "Server error");
  }
}

async function loadDeliveries() {
  const container = document.getElementById("delivery-list");
  container.innerHTML = "Loading...";

  try {
    const res = await fetch(`${API_BASE}/deliveries/`);
    const data = await res.json();

    if (!res.ok) {
      container.innerHTML = "Error loading";
      return;
    }

    deliveriesCache = {};
    data.forEach(d => deliveriesCache[d.delivery_id] = d);

    container.innerHTML = data.map(d => `
      <div class="delivery-card">
        <p><b>ID:</b> ${d.delivery_id}</p>
        <p><b>Status:</b> ${d.status}</p>
        <p><b>ETA:</b> ${d.estimated_arrival || "N/A"}</p>

        <select id="status-${d.delivery_id}">
          <option value="pending">pending</option>
          <option value="assigned">assigned</option>
          <option value="picked_up">picked_up</option>
          <option value="on_the_way">on_the_way</option>
          <option value="delivered">delivered</option>
        </select>

        <button onclick="updateStatus(${d.delivery_id})">Update</button>
        <button onclick="deleteDelivery(${d.delivery_id})">Delete</button>
      </div>
    `).join("");

  } catch {
    container.innerHTML = "Server error";
  }
}

async function updateStatus(id) {
  const status = document.getElementById(`status-${id}`).value;
  const existing = deliveriesCache[id];

  try {
    await fetch(`${API_BASE}/deliveries/${id}/status`, {
      method: "PUT",
      headers: {"Content-Type": "application/json"},
      body: JSON.stringify({
        status,
        estimated_arrival: existing.estimated_arrival
      })
    });

    loadDeliveries();
  } catch {
    alert("Error updating");
  }
}

async function deleteDelivery(id) {
  try {
    await fetch(`${API_BASE}/deliveries/${id}`, { method: "DELETE" });
    loadDeliveries();
  } catch {
    alert("Error deleting");
  }
}