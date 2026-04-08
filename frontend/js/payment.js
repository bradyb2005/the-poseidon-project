// frontend/js/payment.js

let currentOrder = null;
let currentTotal = null;

function renderPaymentPage() {
  const root = document.getElementById("app-root");

  root.innerHTML = `
    <div class="page-card">
      <div class="page-header">
        <h2>💳 Payment</h2>
        <a href="#" onclick="renderHomepage()">Home</a>
      </div>

      <div class="section">
        <h3>Order Details</h3>

        <div class="form-group">
          <label>Price</label>
          <input type="number" id="price" step="0.01">
        </div>

        <div class="form-group">
          <label>Quantity</label>
          <input type="number" id="quantity">
        </div>

        <button onclick="calculate()">Calculate</button>
        <div id="calc-result" class="result-box"></div>
      </div>

      <div class="section">
        <h3>Payment Details</h3>

        <div class="form-group">
          <label>Name</label>
          <input id="card_name">
        </div>

        <div class="form-group">
          <label>Card Number</label>
          <input id="card_number">
        </div>

        <div class="form-group">
          <label>CVV</label>
          <input id="cvv">
        </div>

        <div class="form-group">
          <label>Expiry</label>
          <input id="expiry">
        </div>

        <button onclick="pay()">Pay</button>
        <div id="pay-msg" class="message-box"></div>
      </div>
    </div>
  `;
}

function showMsg(el, text, type) {
  el.textContent = text;
  el.className = `message-box ${type}`;
}

function readValue(obj, key1, key2) {
  const val = obj?.[key1] ?? obj?.[key2];
  return (val !== null && typeof val === "object") ? JSON.stringify(val) : val;
}

async function calculate() {
  const price = parseFloat(document.getElementById("price").value);
  const quantity = parseInt(document.getElementById("quantity").value);
  const box = document.getElementById("calc-result");

  if (isNaN(price) || isNaN(quantity) || price <= 0 || quantity <= 0) {
    box.textContent = "Enter valid values.";
    return;
  }

  currentOrder = {
    items: [{ price, quantity }]
  };

  try {
    const subRes = await fetch(`${API_BASE}/payments/subtotal`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(currentOrder)
    });

    const sub = await subRes.json();

    if (!subRes.ok) {
      box.textContent = JSON.stringify(sub, null, 2);
      return;
    }

    const subtotalValue = readValue(sub, "subtotal", "_subtotal");

    const totalRes = await fetch(`${API_BASE}/payments/total?subtotal=${subtotalValue}`, {
      method: "POST"
    });

    const total = await totalRes.json();

    if (!totalRes.ok) {
      box.textContent = JSON.stringify(total, null, 2);
      return;
    }

    const subtotal = readValue(total, "subtotal", "_subtotal");
    const deliveryFee = readValue(total, "delivery_fee", "_delivery_fee");
    const serviceFee = readValue(total, "service_fee", "_service_fee");
    const tax = readValue(total, "tax", "_tax");
    const grandTotal = readValue(total, "total", "_total");

    currentTotal = Number(grandTotal);

    box.textContent =
`Subtotal: $${subtotal}
Delivery Fee: $${deliveryFee}
Service Fee: $${serviceFee}
Tax: $${tax}
Total: $${grandTotal}

Raw total response:
${JSON.stringify(total, null, 2)}`;
  } catch (err) {
    console.error(err);
    box.textContent = "Error connecting to backend.";
  }
}

async function pay() {
  const msg = document.getElementById("pay-msg");

  if (!currentOrder || Number.isNaN(currentTotal) || currentTotal === null) {
    showMsg(msg, "Calculate first.", "error");
    return;
  }

  const payload = {
    id: Date.now(),
    order: currentOrder,
    card_name: document.getElementById("card_name").value,
    card_number: parseInt(document.getElementById("card_number").value),
    security_number: parseInt(document.getElementById("cvv").value),
    expiration: document.getElementById("expiry").value,
    status: "denied",
    amount: currentTotal
  };

  try {
    const res = await fetch(`${API_BASE}/payments/process`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload)
    });

    const data = await res.json();

    if (!res.ok) {
      showMsg(msg, JSON.stringify(data), "error");
      return;
    }

    if (data.status === "accepted" || data._status === "accepted") {
      const fulfillRes = await fetch(`${API_BASE}/payments/fulfillment`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(data)
      });

      const fulfillData = await fulfillRes.json();

      if (!fulfillRes.ok) {
        showMsg(msg, JSON.stringify(fulfillData), "error");
        return;
      }

      showMsg(msg, "Payment successful 🎉", "success");
    } else {
      showMsg(msg, "Payment denied.", "error");
    }
  } catch (err) {
    console.error(err);
    showMsg(msg, "Backend error.", "error");
  }
}