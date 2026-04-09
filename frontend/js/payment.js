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
  const calcBox = document.getElementById("calc");

  if (!price || !quantity) {
    calcBox.innerText = "Enter valid price and quantity";
    return;
  }

  currentOrder = {
    items: [{ price_at_time: price, quantity }]
  };

  try {
    const sub = await fetch(`${API_BASE}/payments/subtotal`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(currentOrder)
    });

    const subData = await sub.json();

    if (!sub.ok) {
      calcBox.innerText = JSON.stringify(subData);
      return;
    }

    const subtotal = subData.subtotal ?? subData._subtotal;

    const total = await fetch(`${API_BASE}/payments/total`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(subtotal)
    });

    const totalData = await total.json();

    if (!total.ok) {
      calcBox.innerText = JSON.stringify(totalData);
      return;
    }

    const breakdownSubtotal = totalData.subtotal ?? totalData._subtotal;
    const deliveryFee = totalData.delivery_fee ?? totalData._delivery_fee;
    const serviceFee = totalData.service_fee ?? totalData._service_fee;
    const tax = totalData.tax ?? totalData._tax;
    const grandTotal = totalData.total ?? totalData._total;

    currentTotal = grandTotal;

    calcBox.innerText =
      `Subtotal: $${breakdownSubtotal}
Delivery Fee: $${deliveryFee}
Service Fee: $${serviceFee}
Tax: $${tax}
Total: $${grandTotal}`;
  } catch (err) {
    console.error(err);
    calcBox.innerText = "Error connecting to backend";
  }
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
      msg.innerText = JSON.stringify(data);
      return;
    }

    if ((data.status ?? data._status) === "accepted") {
      await fetch(`${API_BASE}/payments/fulfillment`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(data)
      });

      msg.innerText = "Success 🎉";
    } else {
      msg.innerText = "Denied";
    }
  } catch (err) {
    console.error(err);
    msg.innerText = "Error processing payment";
  }
}