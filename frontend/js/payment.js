let currentOrder = null;
let currentTotal = null;

function renderPaymentPage() {
  const root = document.getElementById("app-root");

  root.innerHTML = `
    <div class="page-card">
      <h2>💳 Payment</h2>

      <input id="price" placeholder="Price" type="number" />
      <input id="quantity" placeholder="Quantity" type="number" />

      <button onclick="calculate()">Calculate</button>
      <div id="calc"></div>

      <h3>Card</h3>
      <input id="card_name" placeholder="Name" />
      <input id="card_number" placeholder="Card Number" />
      <input id="cvv" placeholder="CVV" />
      <input id="expiry" placeholder="MM/YY" />

      <button onclick="pay()">Pay</button>
      <div id="pay-msg"></div>
    </div>
  `;
}

async function calculate() {
  const price = parseFloat(document.getElementById("price").value);
  const quantity = parseInt(document.getElementById("quantity").value);

  if (!price || !quantity) return;

  currentOrder = { items: [{ price, quantity }] };

  const sub = await fetch(`${API_BASE}/payments/subtotal`, {
    method: "POST",
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify(currentOrder)
  });

  const subData = await sub.json();

  const total = await fetch(`${API_BASE}/payments/total?subtotal=${subData.subtotal}`, {
    method: "POST"
  });

  const totalData = await total.json();

  currentTotal = totalData.total;

  document.getElementById("calc").innerText =
    `Total: $${currentTotal}`;
}

async function pay() {
  const msg = document.getElementById("pay-msg");

  if (!currentOrder || currentTotal === null) {
    msg.innerText = "Calculate first";
    return;
  }

  const payload = {
    id: Date.now(),
    order: currentOrder,
    card_name: document.getElementById("card_name").value,
    card_number: document.getElementById("card_number").value, // STRING ✅
    security_number: document.getElementById("cvv").value,
    expiration: document.getElementById("expiry").value,
    status: "pending", // ✅
    amount: currentTotal
  };

  const res = await fetch(`${API_BASE}/payments/process`, {
    method: "POST",
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify(payload)
  });

  const data = await res.json();

  if (data.status === "accepted") {
    await fetch(`${API_BASE}/payments/fulfillment`, {
      method: "POST",
      headers: {"Content-Type": "application/json"},
      body: JSON.stringify(data)
    });

    msg.innerText = "Success 🎉";
  } else {
    msg.innerText = "Denied";
  }
}