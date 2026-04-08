// frontend/js/forgot_password.js

function renderForgotPassword() {
  const root = document.getElementById("app-root");

  root.innerHTML = `
    <div class="card">
      <h1>🔱 Reset Password</h1>
      <p style="text-align:center; color:#666; margin-bottom:1.5rem; font-size:0.9rem;">
        Enter the email address on your account and choose a new password.
      </p>

      <div class="form-group">
        <label for="email">Email</label>
        <input type="email" id="email" placeholder="Enter your email">
      </div>

      <div class="form-group">
        <label for="new_password">New Password</label>
        <input type="password" id="new_password" placeholder="Choose a new password">
      </div>

      <div class="form-group">
        <label for="confirm">Confirm New Password</label>
        <input type="password" id="confirm" placeholder="Repeat new password">
      </div>

      <button onclick="handleForgotPassword()">Reset Password</button>

      <div class="message" id="message"></div>

      <div class="link">
        Remembered it? <a href="#" onclick="renderLogin()">Back to login</a>
      </div>
    </div>
  `;

  document.addEventListener("keydown", function onEnter(e) {
    if (e.key === "Enter") handleForgotPassword();
  });
}

async function handleForgotPassword() {
  const email = document.getElementById("email").value.trim();
  const new_password = document.getElementById("new_password").value.trim();
  const confirm = document.getElementById("confirm").value.trim();
  const msg = document.getElementById("message");

  if (!email || !new_password || !confirm) {
    showMessage(msg, "Please fill in all fields.", "error");
    return;
  }

  if (new_password !== confirm) {
    showMessage(msg, "Passwords do not match.", "error");
    return;
  }

  if (new_password.length < 6) {
    showMessage(msg, "Password must be at least 6 characters.", "error");
    return;
  }

  try {
    const response = await fetch(`${API_BASE}/users/forgot-password`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ email, new_password })
    });

    const data = await response.json();

    if (response.ok) {
      showMessage(msg, "Password reset! Redirecting to login...", "success");
      setTimeout(() => renderLogin(), 1500);
    } else {
      showMessage(msg, data.detail || "Reset failed.", "error");
    }

  } catch (err) {
    showMessage(msg, "Cannot reach server. Is the backend running?", "error");
  }
}

function showMessage(el, text, type) {
  el.textContent = text;
  el.className = `message ${type}`;
  el.style.display = "block";
}
