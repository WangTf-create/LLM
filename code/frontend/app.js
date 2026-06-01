// 前端实现 — 驱动: openapi.json + spec/todo_ui_spec.md

const API_BASE = window.location.origin;
const TOKEN_KEY = "access_token";

const main = document.getElementById("main");
const nav = document.getElementById("nav");
const toastEl = document.getElementById("toast");

function getToken() {
  return localStorage.getItem(TOKEN_KEY);
}

function setToken(token) {
  localStorage.setItem(TOKEN_KEY, token);
}

function clearToken() {
  localStorage.removeItem(TOKEN_KEY);
}

function showToast(message) {
  toastEl.textContent = message;
  toastEl.classList.remove("hidden");
  setTimeout(() => toastEl.classList.add("hidden"), 3000);
}

function parseRoute() {
  const hash = window.location.hash.slice(1) || "/login";
  const parts = hash.split("/").filter(Boolean);
  return { parts, raw: hash };
}

function navigate(path) {
  window.location.hash = path;
}

function escapeHtml(text) {
  return String(text)
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;");
}

function renderRecordPanel({ creator, completer, showCompleter }) {
  const completerValue = completer
    ? escapeHtml(completer)
    : '<span class="record-value muted">待完成</span>';
  const completerBlock = showCompleter
    ? `
      <div class="record-item">
        <span class="record-label">完成者</span>
        ${completer ? `<span class="record-value">${escapeHtml(completer)}</span>` : completerValue}
      </div>
    `
    : "";

  return `
    <div class="record-panel">
      <p class="record-panel-title">协作记录</p>
      <div class="record-grid">
        <div class="record-item">
          <span class="record-label">创建者</span>
          <span class="record-value">${escapeHtml(creator || "未知")}</span>
        </div>
        ${completerBlock}
      </div>
    </div>
  `;
}

function renderNav(loggedIn) {
  if (!loggedIn) {
    nav.innerHTML = "";
    return;
  }
  nav.innerHTML = `
    <a class="nav-btn" href="#/teams">我的团队</a>
    <a class="nav-btn" href="#" id="logout">退出</a>
  `;
  document.getElementById("logout").addEventListener("click", (e) => {
    e.preventDefault();
    clearToken();
    navigate("/login");
    render();
  });
}

async function api(path, options = {}) {
  const authRequired = options.authRequired !== false;
  const headers = { "Content-Type": "application/json", ...(options.headers || {}) };
  const token = getToken();
  if (token) {
    headers.Authorization = `Bearer ${token}`;
  }
  const response = await fetch(`${API_BASE}${path}`, { ...options, headers });
  if (response.status === 401 && authRequired) {
    clearToken();
    navigate("/login");
    render();
    throw new Error("Session expired");
  }
  if (response.status === 403) {
    showToast("无权限访问");
    throw new Error("Forbidden");
  }
  if (response.status === 404) {
    showToast("资源不存在");
    throw new Error("Not found");
  }
  let data = null;
  const text = await response.text();
  if (text) {
    data = JSON.parse(text);
  }
  if (!response.ok) {
    const detail = data?.detail;
    const message = typeof detail === "string" ? detail : JSON.stringify(detail);
    throw new Error(message || `HTTP ${response.status}`);
  }
  return { data, status: response.status };
}

function requireAuth() {
  if (!getToken()) {
    navigate("/login");
    return false;
  }
  return true;
}

function renderLogin() {
  main.innerHTML = `
    <div class="auth-wrap">
      <div class="card auth-card">
        <h2>登录</h2>
        <p class="auth-desc">登录后进入团队工作区，协作管理待办。</p>
        <div class="form-group">
          <label for="username">用户名</label>
          <input id="username" type="text" autocomplete="username">
        </div>
        <div class="form-group">
          <label for="password">密码</label>
          <input id="password" type="password" autocomplete="current-password">
        </div>
        <button id="login-btn" disabled>登录</button>
        <div id="error" class="error"></div>
        <p class="muted">还没有账号？<a href="#/register">立即注册</a></p>
      </div>
    </div>
  `;
  const usernameInput = document.getElementById("username");
  const passwordInput = document.getElementById("password");
  const loginBtn = document.getElementById("login-btn");
  const errorEl = document.getElementById("error");

  function updateBtn() {
    loginBtn.disabled = !usernameInput.value.trim() || !passwordInput.value;
  }
  usernameInput.addEventListener("input", updateBtn);
  passwordInput.addEventListener("input", updateBtn);

  loginBtn.addEventListener("click", async () => {
    errorEl.textContent = "";
    try {
      const { data } = await api("/auth/login", {
        method: "POST",
        authRequired: false,
        body: JSON.stringify({
          username: usernameInput.value.trim(),
          password: passwordInput.value,
        }),
      });
      setToken(data.access_token);
      navigate("/teams");
      render();
    } catch (err) {
      if (err.message !== "Session expired") {
        errorEl.textContent = err.message;
      }
    }
  });
}

function renderRegister() {
  main.innerHTML = `
    <div class="auth-wrap">
      <div class="card auth-card">
        <h2>注册</h2>
        <p class="auth-desc">创建账号后即可创建团队并邀请成员。</p>
        <div class="form-group">
          <label for="username">用户名</label>
          <input id="username" type="text" autocomplete="username">
        </div>
        <div class="form-group">
          <label for="password">密码</label>
          <input id="password" type="password" autocomplete="new-password">
        </div>
        <button id="register-btn">注册并登录</button>
        <div id="error" class="error"></div>
        <p class="muted">已有账号？<a href="#/login">返回登录</a></p>
      </div>
    </div>
  `;
  const usernameInput = document.getElementById("username");
  const passwordInput = document.getElementById("password");
  const registerBtn = document.getElementById("register-btn");
  const errorEl = document.getElementById("error");

  registerBtn.addEventListener("click", async () => {
    errorEl.textContent = "";
    try {
      await api("/auth/register", {
        method: "POST",
        authRequired: false,
        body: JSON.stringify({
          username: usernameInput.value.trim(),
          password: passwordInput.value,
        }),
      });
      const { data } = await api("/auth/login", {
        method: "POST",
        authRequired: false,
        body: JSON.stringify({
          username: usernameInput.value.trim(),
          password: passwordInput.value,
        }),
      });
      setToken(data.access_token);
      navigate("/teams");
      render();
    } catch (err) {
      if (err.message !== "Session expired") {
        errorEl.textContent = err.message;
      }
    }
  });
}

async function renderTeams() {
  if (!requireAuth()) {
    return;
  }
  main.innerHTML = `
    <div class="page-header">
      <h2>我的团队</h2>
      <p>每个团队卡片下方都有独立的协作记录区域，展示团队创建者。</p>
    </div>
    <div class="card">
      <ul id="team-list" class="list"></ul>
      <p id="empty" class="empty-box hidden">还没有团队，在下方创建第一个团队工作区。</p>
      <div class="panel">
        <h3>创建新团队</h3>
        <div class="inline-form">
          <input id="team-name" type="text" maxlength="50" placeholder="输入团队名称">
          <button id="create-team">创建团队</button>
        </div>
      </div>
      <div id="error" class="error"></div>
    </div>
  `;
  const listEl = document.getElementById("team-list");
  const emptyEl = document.getElementById("empty");
  const nameInput = document.getElementById("team-name");
  const errorEl = document.getElementById("error");

  async function loadTeams() {
    try {
      const { data } = await api("/teams");
      listEl.innerHTML = "";
      if (data.length === 0) {
        emptyEl.classList.remove("hidden");
        return;
      }
      emptyEl.classList.add("hidden");
      data.forEach((team) => {
        const li = document.createElement("li");
        li.className = "entity-card";
        li.innerHTML = `
          <div class="entity-head">
            <h3 class="entity-title">
              <a href="#/teams/${team.id}/todos">${escapeHtml(team.name)}</a>
            </h3>
            <a class="btn" href="#/teams/${team.id}/todos">进入待办</a>
          </div>
          ${renderRecordPanel({
            creator: team.created_by_username,
            showCompleter: false,
          })}
        `;
        listEl.appendChild(li);
      });
    } catch (err) {
      if (err.message !== "Session expired" && err.message !== "Forbidden" && err.message !== "Not found") {
        errorEl.textContent = err.message;
      }
    }
  }

  document.getElementById("create-team").addEventListener("click", async () => {
    errorEl.textContent = "";
    const name = nameInput.value.trim();
    if (!name) {
      return;
    }
    try {
      await api("/teams", {
        method: "POST",
        body: JSON.stringify({ name }),
      });
      nameInput.value = "";
      await loadTeams();
    } catch (err) {
      if (err.message !== "Session expired" && err.message !== "Forbidden" && err.message !== "Not found") {
        errorEl.textContent = err.message;
      }
    }
  });

  await loadTeams();
}

async function renderTodos(teamId) {
  if (!requireAuth()) {
    return;
  }
  main.innerHTML = `
    <div class="page-header">
      <a class="back-link" href="#/teams">&larr; 返回团队列表</a>
      <h2 id="team-title">团队待办</h2>
      <p>每条待办都有独立的协作记录区域，分别展示创建者与完成者。</p>
    </div>
    <div class="card">
      <ul id="todo-list" class="list"></ul>
      <p id="empty" class="empty-box hidden">还没有待办，在下方添加第一条。</p>
      <div class="panel">
        <h3>新建待办</h3>
        <div class="inline-form">
          <input id="todo-title" type="text" maxlength="100" placeholder="输入待办标题（最多 100 字）">
          <button id="add-todo" disabled>添加</button>
        </div>
      </div>
      <div id="error" class="error"></div>
    </div>
  `;
  const listEl = document.getElementById("todo-list");
  const emptyEl = document.getElementById("empty");
  const titleInput = document.getElementById("todo-title");
  const addBtn = document.getElementById("add-todo");
  const errorEl = document.getElementById("error");
  const teamTitleEl = document.getElementById("team-title");

  try {
    const { data: team } = await api(`/teams/${teamId}`);
    teamTitleEl.textContent = `${team.name} · 待办列表`;
  } catch (err) {
    if (err.message !== "Session expired" && err.message !== "Forbidden" && err.message !== "Not found") {
      errorEl.textContent = err.message;
    }
  }

  titleInput.addEventListener("input", () => {
    addBtn.disabled = !titleInput.value.trim();
  });

  async function loadTodos() {
    try {
      const { data } = await api(`/teams/${teamId}/todos`);
      listEl.innerHTML = "";
      if (data.length === 0) {
        emptyEl.classList.remove("hidden");
        return;
      }
      emptyEl.classList.add("hidden");
      data.forEach((todo) => {
        const li = document.createElement("li");
        li.className = "entity-card";
        const titleClass = todo.done ? "entity-title done" : "entity-title";
        const badge = todo.done
          ? '<span class="status-badge done">已完成</span>'
          : '<span class="status-badge pending">进行中</span>';
        li.innerHTML = `
          <div class="entity-head">
            <h3 class="${titleClass}">${escapeHtml(todo.title)}</h3>
            ${badge}
          </div>
          ${renderRecordPanel({
            creator: todo.created_by_username,
            completer: todo.completed_by_username,
            showCompleter: true,
          })}
          <div class="entity-actions"></div>
        `;
        const actions = li.querySelector(".entity-actions");
        if (!todo.done) {
          const doneBtn = document.createElement("button");
          doneBtn.textContent = "标记完成";
          doneBtn.className = "secondary";
          doneBtn.addEventListener("click", async () => {
            await api(`/teams/${teamId}/todos/${todo.id}/done`, { method: "POST" });
            await loadTodos();
          });
          actions.appendChild(doneBtn);
        }
        const editBtn = document.createElement("button");
        editBtn.textContent = "编辑标题";
        editBtn.className = "ghost";
        editBtn.addEventListener("click", async () => {
          const next = prompt("编辑待办标题", todo.title);
          if (next === null) {
            return;
          }
          if (!next.trim()) {
            showToast("标题不能为空");
            return;
          }
          await api(`/teams/${teamId}/todos/${todo.id}`, {
            method: "PATCH",
            body: JSON.stringify({ title: next.trim() }),
          });
          await loadTodos();
        });
        actions.appendChild(editBtn);
        const delBtn = document.createElement("button");
        delBtn.textContent = "删除";
        delBtn.className = "danger";
        delBtn.addEventListener("click", async () => {
          if (!confirm("确定删除这条待办吗？")) {
            return;
          }
          await api(`/teams/${teamId}/todos/${todo.id}`, { method: "DELETE" });
          await loadTodos();
        });
        actions.appendChild(delBtn);
        listEl.appendChild(li);
      });
    } catch (err) {
      if (err.message !== "Session expired" && err.message !== "Forbidden" && err.message !== "Not found") {
        errorEl.textContent = err.message;
      }
    }
  }

  addBtn.addEventListener("click", async () => {
    errorEl.textContent = "";
    try {
      await api(`/teams/${teamId}/todos`, {
        method: "POST",
        body: JSON.stringify({ title: titleInput.value.trim() }),
      });
      titleInput.value = "";
      addBtn.disabled = true;
      await loadTodos();
    } catch (err) {
      if (err.message !== "Session expired" && err.message !== "Forbidden" && err.message !== "Not found") {
        errorEl.textContent = err.message;
      }
    }
  });

  await loadTodos();
}

function render() {
  const { parts } = parseRoute();
  const loggedIn = !!getToken();
  renderNav(loggedIn);

  if (parts[0] === "login") {
    renderLogin();
    return;
  }
  if (parts[0] === "register") {
    renderRegister();
    return;
  }
  if (parts[0] === "teams") {
    if (parts.length === 1) {
      renderTeams();
      return;
    }
    if (parts.length === 3 && parts[2] === "todos") {
      const teamId = parseInt(parts[1], 10);
      if (Number.isNaN(teamId)) {
        navigate("/teams");
        return;
      }
      renderTodos(teamId);
      return;
    }
  }
  navigate(loggedIn ? "/teams" : "/login");
}

window.addEventListener("hashchange", render);
render();
