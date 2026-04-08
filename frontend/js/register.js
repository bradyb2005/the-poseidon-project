// frontend/js/register.js

function renderRegister() {
  const root = document.getElementById("app-root");

  root.innerHTML = `
    <div class="card">
      <h1>🔱 Create Account</h1>

      <div class="form-group">
        <label for="username">Username</label>
        <input type="text" id="username" placeholder="Choose a username">
      </div>

      <div class="form-group">
        <label for="email">Email</label>
        <input type="email" id="email" placeholder="Enter your email">
      </div>

      <div class="form-group">
        <label for="password">Password</label>
        <input type="password" id="password" placeholder="Choose a password">
      </div>

      <div class="form-group">
        <label for="confirm">Confirm Password</label>
        <input type="password" id="confirm" placeholder="Repeat your password">
      </div>

      <button onclick="handleRegister()">Create Account</button>

      <div class="message" id="message"></div>

      <div class="link">
        Already have an account? <a href="#" onclick="renderLogin()">Log in</a>
      </div>
    </div>
  `;

  document.addEventListener("keydown", function onEnter(e) {
    if (e.key === "Enter") handleRegister();
  });
}

async function handleRegister() {
  const username = document.getElementById("username").value.trim();
  const email = document.getElementById("email").value.trim();
  const password = document.getElementById("password").value.trim();
  const confirm = document.getElementById("confirm").value.trim();
  const msg = document.getElementById("message");

  if (!username || !email || !password || !confirm) {
    showMessage(msg, "Please fill in all fields.", "error");
    return;
  }

  if (password !== confirm) {
    showMessage(msg, "Passwords do not match.", "error");
    return;
  }

  if (password.length < 6) {
    showMessage(msg, "Password must be at least 6 characters.", "error");
    return;
  }

  try {
    const response = await fetch(`${API_BASE}/users/register`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ username, email, password })
    });

    const data = await response.json();

    if (response.ok) {
      localStorage.setItem("user", JSON.stringify(data.user));
      showMessage(msg, "Account created! Redirecting...", "success");
      setTimeout(() => renderNotifications(), 1000);
    } else {
      showMessage(msg, data.detail || "Registration failed.", "error");
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
