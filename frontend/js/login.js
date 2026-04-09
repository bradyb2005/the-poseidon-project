// frontend/js/login.js

function renderLogin() {
  const root = document.getElementById("app-root");

  root.innerHTML = `
    <div class="card">
      <h1>🔱 Poseidon</h1>
      <form>
        <div class="form-group">
          <label for="username">Username</label>
          <input type="text" id="username" placeholder="Enter your username">
        </div>

        <div class="form-group">
          <label for="password">Password</label>
          <input type="password" id="password" placeholder="Enter your password">
        </div>

        <button type="submit">Log In</button>

        <div class="message" id="message"></div>
      </form>

      <div class="link">
        <a href="#" onclick="renderForgotPassword()">Forgot password?</a>
        &nbsp;·&nbsp;
        <a href="#" onclick="renderRegister()">Create account</a>
      </div>
    </div>
  `;

  const form = document.querySelector(".card form");
  if (form) {
    form.addEventListener("submit", function(e) {
      e.preventDefault();
      handleLogin();
    });
  }
}

async function handleLogin() {
  const username = document.getElementById("username").value.trim();
  const password = document.getElementById("password").value.trim();
  const msg = document.getElementById("message");

  if (!username || !password) {
    showMessage(msg, "Please fill in all fields.", "error");
    return;
  }

  try {
    const response = await fetch(`${API_BASE}/users/login`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ username, password })
    });

    const data = await response.json();

    if (response.ok) {
    localStorage.setItem("user", JSON.stringify(data.user));
    showMessage(msg, "Login successful! Redirecting...", "success");
    setTimeout(() => {
        updateNav();
        renderHomepage();
    }, 1000);
    }else {
      showMessage(msg, data.detail || "Login failed.", "error");
    }

  } catch (err) {
    showMessage(msg, "Cannot reach server. Is the backend running?", "error");
  }
}

function showMessage(el, text, type) {
  el.textContent = text;
  el.className = `message ${type}`;
  el.style.display = "block";
  el.onclick = () => { el.style.display = "none"; };
}