/**
 * bulllens/static/js/app.js
 * =========================
 * BullLens – Full SPA Logic
 * DEV_MODE: set to false once Agent 1 marks API endpoints stable in API_CONTRACT.md
 * CACHE_BUST: 2026-03-24-v2
 */

"use strict";

// ================================================================
// 1. DEV MODE FLAG — flip to false to use the real backend API
// ================================================================
const DEV_MODE = false;

// ================================================================
// 2. MOCK DATA — realistic sample data for all views
// ================================================================
const MOCK = {

  watchlist: [
    {
      id: 1,
      symbol: "RELIANCE.NS",
      company_name: "Reliance Industries",
      domain: "ril.com",
      latest_price: 2847.35,
      change_pct: 1.24
    },
    {
      id: 2,
      symbol: "TCS.NS",
      company_name: "Tata Consultancy Services",
      domain: "tcs.com",
      latest_price: 3561.80,
      change_pct: -0.73
    },
    {
      id: 3,
      symbol: "INFY.NS",
      company_name: "Infosys Ltd",
      domain: "infosys.com",
      latest_price: 1438.50,
      change_pct: 2.05
    }
  ],

  stockData: {
    symbol: "RELIANCE.NS",
    company_name: "Reliance Industries",
    domain: "ril.com",
    latest_price: 2847.35,
    change_pct: 1.24,
    labels: generateDateRange(30),
    prices: generatePriceSeries(30, 2700, 2900),
    history: generateHistory(30, 2700, 2900)
  },

  volatility: {
    symbol: "RELIANCE.NS",
    horizon: 10,
    predicted_volatility: 2.14,
    cv_score: 0.38,
    unit: "%"
  },

  price: {
    symbol: "TCS.NS",
    predicted_price: 3720.50,
    confidence_interval: { low: 3580.00, high: 3860.00 },
    horizon_days: 7,
    model_used: "GradientBoostingRegressor"
  }
};

// Helper: generate an array of date strings going back N days
function generateDateRange(n) {
  const dates = [];
  const today = new Date();
  for (let i = n - 1; i >= 0; i--) {
    const d = new Date(today);
    d.setDate(d.getDate() - i);
    dates.push(d.toISOString().slice(0, 10));
  }
  return dates;
}

// Helper: generate a realistic random-walk price series
function generatePriceSeries(n, min, max) {
  const prices = [];
  let price = min + Math.random() * (max - min);
  for (let i = 0; i < n; i++) {
    price += (Math.random() - 0.48) * (max - min) * 0.04;
    price = Math.max(min * 0.95, Math.min(max * 1.05, price));
    prices.push(+price.toFixed(2));
  }
  return prices;
}

// Helper: generate OHLCV history array (for mock stockData.history)
function generateHistory(n, min, max) {
  const dates = generateDateRange(n);
  const closes = generatePriceSeries(n, min, max);
  return dates.map((date, i) => {
    const c = closes[i];
    const o = +(c * (0.99 + Math.random() * 0.02)).toFixed(2);
    const h = +(Math.max(c, o) * (1 + Math.random() * 0.01)).toFixed(2);
    const l = +(Math.min(c, o) * (1 - Math.random() * 0.01)).toFixed(2);
    return { date, open: o, high: h, low: l, close: c, volume: Math.floor(Math.random() * 5e6 + 1e6) };
  });
}

// ================================================================
// 3. MOCK RESOLVER — maps path → MOCK slice
// ================================================================
function resolveMock(path, options = {}) {
  const method = (options.method || "GET").toUpperCase();

  // GET /watchlist
  if (path === "/watchlist" && method === "GET") {
    return mockResponse(200, [...MOCK.watchlist]);
  }

  // POST /add-watchlist
  if (path === "/add-watchlist" && method === "POST") {
    let body = {};
    try { body = JSON.parse(options.body || "{}"); } catch (_) {}
    const sym = (body.symbol || "").toUpperCase().replace(".NS", "");
    const known = ["RELIANCE", "TCS", "INFY", "HDFCBANK", "WIPRO", "ICICIBANK",
                   "BAJFINANCE", "HINDUNILVR", "MARUTI", "SUNPHARMA", "LT", "KOTAKBANK"];
    if (!known.includes(sym)) {
      return mockResponse(400, { error: "symbol_not_found" });
    }
    const newItem = {
      id: Date.now(),
      symbol: sym + ".NS",
      company_name: sym.charAt(0) + sym.slice(1).toLowerCase() + " Ltd",
      domain: sym.toLowerCase() + ".com",
      latest_price: +(1500 + Math.random() * 2000).toFixed(2),
      change_pct: +(Math.random() * 4 - 2).toFixed(2)
    };
    MOCK.watchlist.push(newItem);
    return mockResponse(201, newItem);
  }

  // DELETE /remove-watchlist/<id>
  if (path.startsWith("/remove-watchlist/") && method === "DELETE") {
    const id = parseInt(path.split("/").pop(), 10);
    const idx = MOCK.watchlist.findIndex(w => w.id === id);
    if (idx !== -1) MOCK.watchlist.splice(idx, 1);
    return mockResponse(200, { message: "Removed" });
  }

  // GET /stock-data/<symbol>
  if (path.startsWith("/stock-data/")) {
    const raw = decodeURIComponent(path.split("/stock-data/")[1].split("?")[0]);
    const sym = raw.toUpperCase().replace(/\.NS$/, "");
    const mockD = { ...MOCK.stockData };
    mockD.symbol = sym + ".NS";
    mockD.company_name = sym.charAt(0) + sym.slice(1).toLowerCase() + " Industries";
    mockD.labels = generateDateRange(30);
    mockD.prices = generatePriceSeries(30, 1800, 3200);
    mockD.latest_price = mockD.prices[mockD.prices.length - 1];
    mockD.change_pct = +((Math.random() * 5 - 2).toFixed(2));
    return mockResponse(200, mockD);
  }

  // POST /ml/volatility-predict
  if (path === "/ml/volatility-predict" && method === "POST") {
    let body = {};
    try { body = JSON.parse(options.body || "{}"); } catch (_) {}
    const horizon = parseInt(body.horizon, 10) || 10;
    return mockResponse(200, {
      symbol: (body.symbol || "RELIANCE").toUpperCase() + ".NS",
      horizon,
      predicted_volatility: +(1 + Math.random() * 3.5).toFixed(3),
      cv_score: +(0.2 + Math.random() * 0.5).toFixed(3),
      unit: "%"
    });
  }

  // POST /ml/price-predict
  if (path === "/ml/price-predict" && method === "POST") {
    let body = {};
    try { body = JSON.parse(options.body || "{}"); } catch (_) {}
    const base = 2000 + Math.random() * 2000;
    return mockResponse(200, {
      symbol: (body.symbol || "TCS").toUpperCase() + ".NS",
      predicted_price: +base.toFixed(2),
      confidence_interval: {
        low: +(base * 0.96).toFixed(2),
        high: +(base * 1.04).toFixed(2)
      },
      horizon_days: 7,
      model_used: "GradientBoostingRegressor"
    });
  }

  // Fallback
  return mockResponse(404, { error: "mock_not_found", path });
}

// Create a mock Response-like promise
function mockResponse(status, data) {
  return Promise.resolve({
    ok: status >= 200 && status < 300,
    status,
    json: () => Promise.resolve(data)
  });
}

// ================================================================
// 4. UNIFIED API FUNCTION
// ================================================================
async function api(path, options = {}) {
  if (DEV_MODE) {
    // Artificial 200ms latency to simulate network
    await new Promise(r => setTimeout(r, 200));
    return resolveMock(path, options);
  }
  // Live mode — real fetch
  const res = await fetch(path, {
    headers: { "Content-Type": "application/json", ...(options.headers || {}) },
    ...options
  });
  return {
    ok: res.ok,
    status: res.status,
    json: () => res.json()
  };
}

// ================================================================
// 5. UTILITIES
// ================================================================
const qs    = sel => document.querySelector(sel);
const qsAll = sel => document.querySelectorAll(sel);

/** Format number as Indian Rupee string: ₹ X,XX,XXX.XX */
function formatINR(num) {
  if (num == null || isNaN(num)) return "₹ –";
  const n = parseFloat(num);
  const abs = Math.abs(n);
  const intPart = Math.floor(abs);
  const dec = (abs - intPart).toFixed(2).slice(1); // ".XX"

  // Indian grouping: last 3 digits then groups of 2
  let s = String(intPart);
  if (s.length > 3) {
    const last3 = s.slice(-3);
    const rest  = s.slice(0, -3).replace(/\B(?=(\d{2})+(?!\d))/g, ",");
    s = rest + "," + last3;
  }
  return (n < 0 ? "–₹ " : "₹ ") + s + dec;
}

function escapeHtml(str) {
  return String(str).replace(/[&<>"']/g, m =>
    ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#039;" })[m]
  );
}

/** Show a toast notification — never use alert() */
function showToast(message, type = "info", duration = 3500) {
  const icons = { success: "✅", error: "❌", info: "ℹ️" };
  const container = qs("#toast-container");
  const toast = document.createElement("div");
  toast.className = `bl-toast ${type}`;
  toast.innerHTML = `<span>${icons[type] || "ℹ️"}</span><span>${escapeHtml(message)}</span>`;
  container.appendChild(toast);
  setTimeout(() => {
    toast.style.opacity = "0";
    toast.style.transition = "opacity 0.3s";
    setTimeout(() => toast.remove(), 320);
  }, duration);
}

/**
 * Render logo: tries Clearbit CDN image; on error uses coloured circle with initials.
 * @param {HTMLElement} container  - element to place logo inside
 * @param {string} symbol          - e.g. "RELIANCE.NS"
 * @param {string} [domain]        - e.g. "ril.com"; if omitted, derived from symbol
 */
function renderLogo(container, symbol, domain) {
  const sym = symbol.replace(".NS", "").replace(".BSE", "");
  const initials = sym.slice(0, 2).toUpperCase();
  const colors = ["#1FB28C", "#6366f1", "#f59e0b", "#ef4444", "#3b82f6", "#8b5cf6", "#ec4899"];
  const color  = colors[sym.charCodeAt(0) % colors.length];

  const d = domain || sym.toLowerCase() + ".com";
  const img = document.createElement("img");
  img.src   = `https://logo.clearbit.com/${d}`;
  img.alt   = sym + " logo";
  img.style.cssText = "width:100%;height:100%;object-fit:contain;padding:5px;";
  img.onerror = () => {
    container.innerHTML = "";
    container.style.background = color + "22";
    container.style.color      = color;
    container.style.fontWeight = "700";
    container.style.fontSize   = "0.8rem";
    container.textContent      = initials;
  };
  container.innerHTML = "";
  container.appendChild(img);
}

// ================================================================
// 6. LOGOUT — POST /logout (FastAPI backend requires POST)
// ================================================================
async function doLogout() {
  try {
    await fetch("/logout", { method: "POST" });
  } catch (_) {}
  window.location.href = "/login";
}

// ================================================================
// 7. DARK / LIGHT THEME TOGGLE
// ================================================================
function initTheme() {
  const stored   = localStorage.getItem("bulllens_theme") || "light";
  const iconEl   = qs("#theme-icon");
  setTheme(stored, iconEl);

  qs("#theme-toggle").addEventListener("click", () => {
    const current = document.documentElement.getAttribute("data-theme") || "light";
    const next    = current === "dark" ? "light" : "dark";
    setTheme(next, iconEl);
  });
}

function setTheme(theme, iconEl) {
  document.documentElement.setAttribute("data-theme", theme);
  localStorage.setItem("bulllens_theme", theme);
  if (iconEl) {
    iconEl.className = theme === "dark" ? "fa-solid fa-sun" : "fa-solid fa-moon";
  }
}

// Also update Chart.js defaults on theme change (called from router when theme changes)
function updateChartTheme() {
  const isDark = document.documentElement.getAttribute("data-theme") === "dark";
  Chart.defaults.color          = isDark ? "#94a3b8" : "#6B7280";
  Chart.defaults.scale.grid.color = isDark ? "rgba(255,255,255,0.06)" : "#E5E7EB";
}

// ================================================================
// 7. SPA ROUTER
// ================================================================
const VIEW_MAP = {
  "dashboard": "view-dashboard",
  "watchlist": "view-watchlist",
  "ml":        "view-ml",
  "market":    "view-market",
  "settings":  "view-settings",
  "contact":   "view-contact"
};
const TITLE_MAP = {
  "dashboard": "Dashboard",
  "watchlist": "Watchlist",
  "ml":        "ML Predictions",
  "market":    "Live Market",
  "settings":  "Settings",
  "contact":   "Contact Us"
};

// Track which views have been loaded
const _loaded = {};

function navigateTo(hash) {
  const cleanHash = (hash || "dashboard").replace(/^#/, "");
  const target    = VIEW_MAP[cleanHash] || VIEW_MAP["dashboard"];
  const finalHash = VIEW_MAP[cleanHash] ? cleanHash : "dashboard";

  // Update URL without full reload
  history.pushState({ hash: finalHash }, "", "#" + finalHash);
  applyView(finalHash, target);
}

function applyView(hash, viewId) {
  // Hide all views, activate target
  qsAll(".spa-view").forEach(v => v.classList.remove("active"));
  const targetEl = qs("#" + viewId);
  if (targetEl) targetEl.classList.add("active");

  // Update nav active state
  qsAll(".nav-item").forEach(item => {
    item.classList.toggle("active", item.dataset.hash === hash);
  });

  // Update page title
  const titleEl = qs("#page-title");
  if (titleEl) {
    titleEl.innerHTML = escapeHtml(TITLE_MAP[hash] || "Dashboard") + `
      <div class="cubes">
        <div style="width:11px;height:11px;background:#1FB28C;position:absolute;top:0;left:9px;border-radius:2px;transform:rotate(45deg);"></div>
        <div style="width:11px;height:11px;background:#C4F60D;position:absolute;bottom:0;left:0;border-radius:2px;transform:rotate(45deg);"></div>
        <div style="width:11px;height:11px;background:#0A2523;position:absolute;bottom:0;right:0;border-radius:2px;transform:rotate(45deg);"></div>
      </div>`;
  }

  // Hide search bar on non-dashboard views
  const searchBar = qs("#global-search-bar");
  const searchBtn = qs("#search-btn");
  const show = hash === "dashboard";
  if (searchBar) searchBar.style.display = show ? "" : "none";
  if (searchBtn) searchBtn.style.display = show ? "" : "none";

  // Close mobile sidebar
  closeSidebar();

  // Lazy-load view data (once per session unless forced)
  if (!_loaded[hash]) {
    _loaded[hash] = true;
    updateChartTheme();
    if (hash === "watchlist") loadWatchlistView();
    if (hash === "market")    loadMarketView();
  }
}

function initRouter() {
  // Nav clicks
  qsAll(".nav-item[data-hash]").forEach(item => {
    item.addEventListener("click", () => {
      const hash = item.dataset.hash;
      if (!hash) return; // stub items (settings, contact)
      if (!VIEW_MAP[hash]) return;
      navigateTo(hash);
    });
  });

  // Stub nav items that DO have a view but no hash routing
  qsAll(".nav-item[data-view]").forEach(item => {
    if (!item.dataset.hash) {
      item.addEventListener("click", () => {
        qsAll(".spa-view").forEach(v => v.classList.remove("active"));
        const v = qs("#" + item.dataset.view);
        if (v) v.classList.add("active");
        qsAll(".nav-item").forEach(n => n.classList.remove("active"));
        item.classList.add("active");
        closeSidebar();
      });
    }
  });

  // Browser back/forward
  window.addEventListener("popstate", e => {
    const h = (e.state && e.state.hash) ||
              window.location.hash.replace("#", "") ||
              "dashboard";
    const vid = VIEW_MAP[h] || VIEW_MAP["dashboard"];
    applyView(h, vid);
  });

  // Initial load — read hash from URL
  const initHash = window.location.hash.replace("#", "") || "dashboard";
  const initView = VIEW_MAP[initHash] || VIEW_MAP["dashboard"];
  applyView(initHash, initView);

  // Mobile hamburger
  const hamburger = qs("#hamburger-btn");
  const overlay   = qs("#sidebar-overlay");
  if (hamburger) hamburger.addEventListener("click", openSidebar);
  if (overlay)   overlay.addEventListener("click", closeSidebar);
}

function openSidebar() {
  qs("#sidebar").classList.add("open");
  qs("#sidebar-overlay").classList.add("visible");
}
function closeSidebar() {
  qs("#sidebar").classList.remove("open");
  qs("#sidebar-overlay").classList.remove("visible");
}

// ================================================================
// 8. CHART.JS DEFAULTS
// ================================================================
Chart.defaults.font.family = "'Plus Jakarta Sans', sans-serif";

// ================================================================
// 9. DASHBOARD — Stock Search + Chart
// ================================================================
let priceChart    = null;
let currentSymbol = null;

async function fetchStockData() {
  const rawInput = qs("#symbol-input").value.trim().toUpperCase() || currentSymbol;
  if (!rawInput) { showToast("Enter a stock symbol", "error"); return; }

  const symbol = rawInput.endsWith(".NS") ? rawInput : rawInput + ".NS";
  const period = qs("#period-select") ? qs("#period-select").value : "3mo";
  const title  = qs("#live-chart-title");

  // Loading state
  title.textContent = "Loading…";
  qs("#chart-placeholder").style.display = "none";
  qs("#price-chart").style.display = "none";
  qs("#live-controls").style.display = "none";
  qs("#ml-result-card").style.display = "none";
  qs("#stock-info-strip").style.display = "none";

  try {
    const res  = await api(`/api/stock-data/${encodeURIComponent(symbol)}?period=${period}`);
    const data = await res.json();

    if (!res.ok) {
      showToast(data.detail || "Could not load stock data", "error");
      title.textContent = "Market Analysis — Search a Symbol";
      qs("#chart-placeholder").style.display = "flex";
      return;
    }

    // Extract labels and prices from history
    const labels = data.history.map(d => d.date);
    const prices = data.history.map(d => d.close);

    currentSymbol = data.symbol;
    title.textContent = `${data.symbol}`;

    // Stock info strip
    const strip = qs("#stock-info-strip");
    strip.style.display = "flex";
    strip.style.flexDirection = "column";

    const stripLogo = qs("#strip-logo");
    renderLogo(stripLogo, data.symbol, "");
    qs("#strip-symbol").textContent  = data.symbol.replace(".NS", "");
    qs("#strip-company").textContent = data.symbol;
    qs("#strip-price").textContent   = formatINR(data.latest_price);

    const changeEl = qs("#strip-change");
    const isPos    = data.change_pct >= 0;
    changeEl.textContent = `${isPos ? "▲" : "▼"} ${Math.abs(data.change_pct).toFixed(2)}%`;
    changeEl.style.color = isPos ? "var(--positive)" : "var(--negative)";

    // Render Chart
    qs("#price-chart").style.display = "block";
    qs("#live-controls").style.display = "block";
    renderChart(labels, prices, data.symbol);

    // Save for watchlist action
    qs("#add-watchlist-btn").dataset.symbol  = data.symbol;
    qs("#add-watchlist-btn").dataset.company = data.symbol;
    qs("#add-watchlist-btn").dataset.domain  = "";

  } catch (err) {
    console.error("Stock data fetch error:", err);
    showToast("Network error — check the server", "error");
    title.textContent = "Market Analysis — Search a Symbol";
    qs("#chart-placeholder").style.display = "flex";
  }
}

function renderChart(labels, prices, symbol) {
  const ctx = qs("#price-chart").getContext("2d");
  if (priceChart) priceChart.destroy();

  const min = Math.min(...prices);
  const max = Math.max(...prices);

  const gradient = ctx.createLinearGradient(0, 0, 0, 200);
  gradient.addColorStop(0, "rgba(31, 178, 140, 0.22)");
  gradient.addColorStop(1, "rgba(31, 178, 140, 0)");

  updateChartTheme();

  priceChart = new Chart(ctx, {
    type: "line",
    data: {
      labels,
      datasets: [{
        label: `${symbol} Close`,
        data: prices,
        borderColor: "#1FB28C",
        borderWidth: 2.5,
        pointRadius: 0,
        pointHoverRadius: 6,
        pointHoverBackgroundColor: "#1FB28C",
        fill: true,
        backgroundColor: gradient,
        tension: 0.4
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      interaction: { mode: "index", intersect: false },
      plugins: { legend: { display: false } },
      animation: { duration: 600 },
      scales: {
        x: { display: false },
        y: {
          display: true,
          position: "right",
          border: { display: false },
          ticks: {
            font: { size: 10 },
            callback: v => "₹ " + v.toLocaleString("en-IN")
          },
          suggestedMin: min * 0.99,
          suggestedMax: max * 1.01
        }
      }
    }
  });
}

// ================================================================
// 10. DASHBOARD — YOLO Vision ML Prediction
// ================================================================
async function runMLPrediction() {
  if (!priceChart) return showToast("Fetch a stock chart first", "error");

  qs("#ml-result-card").style.display = "block";
  qs("#ml-result-img").style.display  = "none";
  qs("#ml-result-spinner").style.display = "block";
  qs("#ml-result-stats").innerHTML = "";

  const canvas    = qs("#price-chart");
  const composite = document.createElement("canvas");
  composite.width  = canvas.width;
  composite.height = canvas.height;
  const ctx = composite.getContext("2d");
  ctx.fillStyle = "#ffffff";
  ctx.fillRect(0, 0, composite.width, composite.height);
  ctx.drawImage(canvas, 0, 0);
  const base64 = composite.toDataURL("image/png");

  try {
    const res  = await fetch("/ml/vision-predict", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ image_data: base64, symbol: currentSymbol })
    });
    const data = await res.json();
    if (!res.ok) throw new Error(data.detail || data.error || "ML inference failed");

    qs("#ml-result-spinner").style.display = "none";
    const imgEl = qs("#ml-result-img");
    imgEl.src   = (data.result_image_url || base64) + (data.result_image_url ? "?t=" + Date.now() : "");
    imgEl.style.display = "block";

    const detections = Array.isArray(data.detections_list) ? data.detections_list : [];
    const detectionMarkup = detections.length
      ? detections.map(item => `
          <div style="padding:8px 10px;border:1px solid var(--border);border-radius:10px;background:var(--surface);">
            <strong>${escapeHtml(item.label || "object")}</strong>
            <span style="color:var(--text-muted);margin-left:6px;">${Math.round((item.confidence || 0) * 100)}%</span>
          </div>
        `).join("")
      : `<div style="color:var(--text-muted);">No detections found for this chart image.</div>`;

    qs("#ml-result-stats").innerHTML = `
      <div class="d-flex flex-wrap justify-content-between gap-2 mb-3">
        <span><strong>Detections:</strong> ${data.detections || 0}</span>
        <span><strong>Inference time:</strong> ${data.inference_time_ms || 0} ms</span>
        <span><strong>Model:</strong> YOLOv8 Vision</span>
      </div>
      <div style="display:grid;gap:8px;">${detectionMarkup}</div>`;
    showToast("Prediction complete!", "success");
  } catch (err) {
    qs("#ml-result-spinner").innerHTML =
      `<span style="color:var(--negative);"><i class="fa-solid fa-circle-exclamation me-1"></i>${escapeHtml(err.message)}</span>`;
    showToast(err.message || "Model prediction failed", "error");
  }
}

// ================================================================
// 11. DASHBOARD — Watchlist SIDEBAR widget
// ================================================================
async function loadWatchlist() {
  const wrapper = qs("#watchlist-tbody");
  wrapper.innerHTML = `<div class="text-center py-4" style="color:var(--text-muted);"><span class="spin"></span></div>`;

  try {
    const res  = await api("/api/watchlist");
    const data = await res.json();

    if (!res.ok) { showToast(data.detail || "Failed to load watchlist", "error"); console.error("Watchlist error:", data?.detail); return; }
    if (!data.length) {
      wrapper.innerHTML = `<div class="text-center py-4" style="color:var(--text-muted);">
        <i class="fa-solid fa-folder-open" style="opacity:.4;font-size:1.5rem;display:block;margin-bottom:.5rem;"></i>
        Empty — add stocks from the Watchlist view</div>`;
      return;
    }

    wrapper.innerHTML = data.map(row => {
      const sym   = row.symbol.replace(".NS", "");
      const isPos = row.change_pct >= 0;
      return `
      <div class="list-item">
        <div class="item-logo" id="wl-sidelogo-${row.id}"></div>
        <div class="item-info">
          <div class="item-title">${escapeHtml(sym)}</div>
          <div class="item-sub">${escapeHtml(row.company_name)}</div>
        </div>
        <div class="item-stats ms-auto text-end d-flex align-items-center gap-2">
          <div>
            <div class="item-val">${formatINR(row.latest_price)}</div>
            <div class="item-pct ${isPos ? "pos" : "neg"}">
              ${isPos ? "▲" : "▼"} ${Math.abs(row.change_pct).toFixed(2)}%
            </div>
          </div>
          <button class="add-btn" onclick="quickFetch('${escapeHtml(row.symbol)}')" title="View chart">
            <i class="fa-solid fa-chart-line"></i>
          </button>
          <button class="add-btn remove" onclick="removeFromWatchlist(${row.id})" title="Remove">
            <i class="fa-solid fa-minus"></i>
          </button>
        </div>
      </div>`;
    }).join("");

    // Lazy logo loading
    data.forEach(row => {
      const el = qs(`#wl-sidelogo-${row.id}`);
      if (el) renderLogo(el, row.symbol, row.domain);
    });

  } catch (err) {
    wrapper.innerHTML = `<div class="text-center py-4" style="color:var(--negative);">Network error</div>`;
  }
}

async function addToWatchlist() {
  const btn     = qs("#add-watchlist-btn");
  const symbol  = btn.dataset.symbol;
  const company = btn.dataset.company || symbol;
  const domain  = btn.dataset.domain  || "";
  if (!symbol) return;

  try {
    const res = await api("/api/add-watchlist", {
      method: "POST",
      body: JSON.stringify({ symbol, company_name: company, domain, exchange: "NSE" })
    });
    const data = await res.json();
    if (res.ok || res.status === 409) {
      showToast(res.status === 409 ? "Already in watchlist" : "Added to watchlist ⭐", "success");
      loadWatchlist();
    } else {
      showToast(data.detail || "Could not add to watchlist", "error");
      console.error("Add watchlist error:", data?.detail);
    }
  } catch (e) { showToast(e.message || "Failed to add watchlist", "error"); console.error(e); }
}

async function removeFromWatchlist(id) {
  try {
    const res = await api(`/api/remove-watchlist/${id}`, { method: "DELETE" });
    if (res.ok) { showToast("Removed from watchlist", "success"); loadWatchlist(); }
  } catch (e) {}
}

function quickFetch(symbol) {
  navigateTo("dashboard");
  qs("#symbol-input").value = symbol.replace(".NS", "");
  setTimeout(fetchStockData, 50);
}

// ================================================================
// 12. WATCHLIST VIEW (full page)
// ================================================================
async function loadWatchlistView() {
  const grid = qs("#wl-cards");
  // Skeletons are already in HTML — just wait for data
  try {
    const res  = await api("/api/watchlist");
    const data = await res.json();

    // Clear skeletons
    grid.innerHTML = "";

    if (!res.ok) { showToast(data.detail || "Failed to load watchlist", "error"); console.error("Watchlist error:", data?.detail); return; }

    if (!data.length) {
      grid.style.display = "none";
      qs("#wl-empty").style.display = "block";
      return;
    }

    qs("#wl-empty").style.display = "none";
    grid.style.display = "";
    data.forEach(row => grid.appendChild(makeWatchlistCard(row)));

  } catch (err) {
    grid.innerHTML = `<div style="color:var(--negative);padding:1rem;">Network error — is the server running?</div>`;
  }
}

function makeWatchlistCard(row) {
  const isPos = row.change_pct >= 0;
  const sym   = row.symbol.replace(".NS", "");

  const card = document.createElement("div");
  card.className     = "wl-card";
  card.dataset.wlId  = row.id;
  card.innerHTML = `
    <div class="wl-logo" id="wl-logo-${row.id}"></div>
    <div class="wl-info">
      <div class="wl-symbol">${escapeHtml(sym)}</div>
      <div class="wl-company">${escapeHtml(row.company_name)}</div>
      <div class="wl-price">${formatINR(row.latest_price)}</div>
      <div class="wl-change ${isPos ? "pos" : "neg"}">
        ${isPos ? "▲" : "▼"} ${Math.abs(row.change_pct).toFixed(2)}%
      </div>
    </div>
    <button class="wl-remove" title="Remove from watchlist"
            onclick="removeWatchlistItem(${row.id}, this)">
      <i class="fa-solid fa-times"></i>
    </button>`;

  // Logo after render
  requestAnimationFrame(() => {
    const logoEl = qs(`#wl-logo-${row.id}`);
    if (logoEl) renderLogo(logoEl, row.symbol, row.domain);
  });

  return card;
}

async function addWatchlistItem() {
  const input = qs("#wl-add-input");
  const btn   = qs("#wl-add-btn");
  const errEl = qs("#wl-error");
  const rawSym = input.value.trim().toUpperCase();

  errEl.classList.remove("visible");
  if (!rawSym) { showToast("Enter a symbol first", "error"); return; }

  btn.disabled    = true;
  btn.textContent = "Adding…";

  try {
    const res  = await api("/api/add-watchlist", {
      method: "POST",
      body: JSON.stringify({ symbol: rawSym, company_name: rawSym, exchange: "NSE" })
    });
    const data = await res.json();

    if (res.status === 201) {
      // Append new card without reload
      const grid = qs("#wl-cards");
      grid.style.display = "";
      qs("#wl-empty").style.display = "none";
      grid.appendChild(makeWatchlistCard(data));
      input.value = "";
      showToast("Added to watchlist ⭐", "success");
      // Also refresh sidebar widget
      loadWatchlist();
    } else if (res.status === 400 && data.detail?.includes("not found")) {
      errEl.classList.add("visible");
    } else if (res.status === 409) {
      showToast("Already in watchlist", "info");
    } else {
      showToast(data.detail || "Could not add symbol", "error");
    }
  } catch (err) {
    showToast("Network error", "error");
  } finally {
    btn.disabled    = false;
    btn.innerHTML   = `<i class="fa-solid fa-plus me-1"></i> Add`;
  }
}

async function removeWatchlistItem(id, btnEl) {
  try {
    const res = await api(`/api/remove-watchlist/${id}`, { method: "DELETE" });
    if (res.ok) {
      // Remove card without reload
      const card = btnEl.closest(".wl-card");
      if (card) {
        card.style.transition = "opacity 0.2s, transform 0.2s";
        card.style.opacity    = "0";
        card.style.transform  = "scale(0.95)";
        setTimeout(() => {
          card.remove();
          const grid = qs("#wl-cards");
          if (!grid.querySelector(".wl-card")) {
            grid.style.display = "none";
            qs("#wl-empty").style.display = "block";
          }
        }, 200);
      }
      showToast("Removed from watchlist", "success");
      loadWatchlist(); // refresh sidebar widget
    }
  } catch (e) { showToast("Failed to remove", "error"); }
}

// ================================================================
// 13. ML PREDICTIONS VIEW
// ================================================================
async function runVolatilityPredict() {
  const sym     = qs("#vol-symbol").value.trim().toUpperCase() || "RELIANCE";
  const horizon = qs("#vol-horizon").value;
  const errEl   = qs("#vol-error");
  const resEl   = qs("#vol-result");
  const btn     = qs("#vol-btn");
  const spinner = qs("#vol-spinner");
  const inner   = qs("#vol-result-inner");

  errEl.classList.remove("visible");
  resEl.style.display  = "none";
  btn.disabled         = true;
  btn.textContent      = "Predicting…";

  resEl.style.display = "flex";
  resEl.style.flexDirection = "column";
  spinner.style.setProperty("display", "flex", "important");
  inner.style.display = "none";

  try {
    const res  = await api("/ml/volatility-predict", {
      method: "POST",
      body: JSON.stringify({ symbol: sym, horizon: parseInt(horizon, 10) })
    });
    const data = await res.json();

    spinner.style.setProperty("display", "none", "important");
    inner.style.display = "";

    if (!res.ok) {
      if (data.detail?.includes("insufficient_data") || data.detail?.includes("no_history")) {
        errEl.classList.add("visible");
        qs("#vol-error-msg").textContent = "Not enough historical data for this symbol.";
      } else {
        showToast(data.detail || "Prediction failed", "error");
      }
      resEl.style.display = "none";
      return;
    }

    // Populate result
    qs("#vol-r-symbol").textContent  = data.symbol;
    qs("#vol-r-horizon").textContent = `${data.horizon} days`;
    qs("#vol-r-vol").textContent     = `${data.predicted_volatility.toFixed(3)}%`;
    qs("#vol-r-cv").textContent      = data.cv_score.toFixed(3);

    // Risk label
    const vol = data.predicted_volatility;
    let riskHtml;
    if (vol < 1.5)      riskHtml = `<span class="risk-label risk-low">🟢 Low</span>`;
    else if (vol <= 3)  riskHtml = `<span class="risk-label risk-moderate">🟡 Moderate</span>`;
    else                riskHtml = `<span class="risk-label risk-high">🔴 High</span>`;
    qs("#vol-r-risk").innerHTML = riskHtml;

  } catch (err) {
    console.error(err);
    showToast("Network error", "error");
    resEl.style.display = "none";
  } finally {
    btn.disabled    = false;
    btn.innerHTML   = `<i class="fa-solid fa-bolt me-1"></i> Predict Volatility`;
  }
}

async function runPricePredict() {
  const sym   = qs("#price-symbol").value.trim().toUpperCase() || "TCS";
  const errEl = qs("#price-error");
  const resEl = qs("#price-result");
  const btn   = qs("#price-btn");
  const spinner = qs("#price-spinner");
  const inner   = qs("#price-result-inner");

  errEl.classList.remove("visible");
  resEl.style.display = "none";
  btn.disabled        = true;
  btn.textContent     = "Predicting…";

  resEl.style.display = "flex";
  resEl.style.flexDirection = "column";
  spinner.style.setProperty("display", "flex", "important");
  inner.style.display = "none";

  try {
    const res  = await api("/ml/price-predict", {
      method: "POST",
      body: JSON.stringify({ symbol: sym })
    });
    const data = await res.json();

    spinner.style.setProperty("display", "none", "important");
    inner.style.display = "";

    if (!res.ok) {
      if (data.detail?.includes("insufficient_data") || data.detail?.includes("no_history")) {
        errEl.classList.add("visible");
        qs("#price-error-msg").textContent = "Not enough historical data for this symbol.";
      } else {
        showToast(data.detail || "Prediction failed", "error");
      }
      resEl.style.display = "none";
      return;
    }

    qs("#price-r-symbol").textContent  = data.symbol;
    qs("#price-r-price").textContent   = formatINR(data.predicted_price);
    const ci = data.confidence_interval;
    const ciLow  = Array.isArray(ci) ? ci[0] : ci.low;
    const ciHigh = Array.isArray(ci) ? ci[1] : ci.high;
    qs("#price-r-ci").textContent     = `${formatINR(ciLow)} – ${formatINR(ciHigh)}`;
    qs("#price-r-horizon").textContent = `${data.horizon_days} days`;
    qs("#price-r-model").textContent   = data.model_used;

  } catch (err) {
    console.error(err);
    showToast("Network error", "error");
    resEl.style.display = "none";
  } finally {
    btn.disabled  = false;
    btn.innerHTML = `<i class="fa-solid fa-brain me-1"></i> Predict Price`;
  }
}

// ================================================================
// 14. LIVE MARKET VIEW
// ================================================================
const MARKET_SYMBOLS = [
  { symbol: "RELIANCE.NS", domain: "ril.com" },
  { symbol: "TCS.NS",      domain: "tcs.com" },
  { symbol: "INFY.NS",     domain: "infosys.com" },
  { symbol: "HDFCBANK.NS", domain: "hdfcbank.com" },
  { symbol: "WIPRO.NS",    domain: "wipro.com" },
  { symbol: "ICICIBANK.NS",domain: "icicibank.com" }
];

async function loadMarketView() {
  const grid   = qs("#market-grid");
  const refBtn = qs("#market-refresh-btn");

  // Show skeleton loaders
  grid.innerHTML = MARKET_SYMBOLS.map((_, i) => `
    <div class="skeleton-ticker" id="mkt-skel-${i + 1}">
      <div class="skeleton skeleton-circle"></div>
      <div class="skeleton skeleton-line w80" style="margin-top:6px;"></div>
      <div class="skeleton skeleton-line w50"></div>
      <div class="skeleton skeleton-line w65"></div>
    </div>`).join("");

  if (refBtn) { refBtn.disabled = true; refBtn.style.opacity = "0.6"; }

  try {
    // Fetch all 6 in parallel
    const results = await Promise.allSettled(
      MARKET_SYMBOLS.map(s =>
        api(`/api/stock-data/${encodeURIComponent(s.symbol)}`)
          .then(r => r.json().then(d => ({ ok: r.ok, data: d, meta: s })))
      )
    );

    grid.innerHTML = "";
    let anyError = false;

    results.forEach(result => {
      if (result.status === "rejected") { anyError = true; console.error("Market symbol load error:", result.reason); return; }
      const { ok, data, meta } = result.value;
      if (!ok) {
        anyError = true;
        console.error(`Failed to load ${meta.symbol}:`, data?.detail || "Unknown error");
        return;
      }

      const isPos = data.change_pct >= 0;
      const card  = document.createElement("div");
      card.className = `ticker-card ${isPos ? "pos-tint" : "neg-tint"}`;

      const sym = (data.symbol || meta.symbol).replace(".NS", "");
      card.innerHTML = `
        <div class="ticker-logo" id="mkt-logo-${sym}"></div>
        <div class="ticker-symbol">${escapeHtml(sym)}</div>
        <div class="ticker-price">${formatINR(data.latest_price)}</div>
        <div class="ticker-change ${isPos ? "pos" : "neg"}">
          <i class="fa-solid fa-arrow-trend-${isPos ? "up" : "down"}"></i>
          ${isPos ? "+" : ""}${(data.change_pct || 0).toFixed(2)}%
        </div>`;

      grid.appendChild(card);

      requestAnimationFrame(() => {
        const logoEl = qs(`#mkt-logo-${sym}`);
        if (logoEl) renderLogo(logoEl, meta.symbol, meta.domain);
      });
    });

    if (anyError) showToast("Some stocks could not be loaded", "info");
    if (!grid.children.length) {
      grid.innerHTML = `<div class="market-error">Could not load market data. Is the server running?</div>`;
    }

  } catch (err) {
    grid.innerHTML = `<div class="market-error">Network error — ${escapeHtml(err.message)}</div>`;
  } finally {
    if (refBtn) { refBtn.disabled = false; refBtn.style.opacity = ""; }
  }
}

// ================================================================
// 15. DASHBOARD — Index Quick Picks
// ================================================================
async function fetchIndexQuickPicks() {
  try {
    const res = await fetch("/api/quick-picks");
    if (!res.ok) return;
    const data = await res.json();

    const buildSpark = (id, color, prices) => {
      const el = qs(id);
      if (!el) return;
      new Chart(el, {
        type: "line",
        data: {
          labels: prices.map((_, i) => i),
          datasets: [{ data: prices, borderColor: color, borderWidth: 2, tension: 0.4, pointRadius: 0, fill: false }]
        },
        options: {
          responsive: true, maintainAspectRatio: false,
          plugins: { legend: { display: false }, tooltip: { enabled: false } },
          scales: { x: { display: false }, y: { display: false } }
        }
      });
    };

    const mapping = {
      "^NSEI":    { valId: "#val-nifty", pctId: "#pct-nifty", sparkId: "#spark-nifty" },
      "^NSEBANK": { valId: "#val-bank",  pctId: "#pct-bank",  sparkId: "#spark-bank"  },
      "^CNXIT":   { valId: "#val-it",    pctId: "#pct-it",    sparkId: "#spark-it"    },
      "^CNXFMCG": { valId: "#val-fmcg",  pctId: "#pct-fmcg",  sparkId: "#spark-fmcg"  }
    };

    Object.keys(data).forEach(idx => {
      const m = mapping[idx];
      if (!m) return;
      const d = data[idx];
      const valEl = qs(m.valId);
      const pctEl = qs(m.pctId);
      if (valEl) valEl.textContent = Math.round(d.current).toLocaleString("en-IN");
      if (pctEl) {
        const isPos = d.pct_change >= 0;
        pctEl.className = `mini-pct ${isPos ? "" : "neg"}`;
        pctEl.innerHTML = `<i class="fa-solid fa-arrow-trend-${isPos ? "up" : "down"}"></i> ${isPos ? "+" : ""}${d.pct_change.toFixed(2)}%`;
        buildSpark(m.sparkId, isPos ? "#1FB28C" : "#ef4444", d.history);
      }
    });

  } catch (e) { console.warn("Could not fetch index quick picks", e); }
}

// ================================================================
// 16. DASHBOARD — Gainers / Losers
// ================================================================
async function fetchGainersLosers() {
  try {
    const res = await fetch("/api/gainers-losers");
    if (!res.ok) return;
    window.glData = await res.json();
    switchGLTab("gainers");
  } catch (e) { console.warn("Could not fetch gainers/losers", e); }
}

function switchGLTab(type) {
  if (!window.glData) return;
  const activeTab = qs(".tabs-pill .active");
  if (activeTab) activeTab.classList.remove("active");
  const tab = qs(`#tab-${type}`);
  if (tab) tab.classList.add("active");

  const arr     = window.glData[type] || [];
  const wrapper = qs("#gl-body");
  if (!wrapper) return;

  if (!arr.length) {
    wrapper.innerHTML = `<div class="text-center py-4" style="color:var(--text-muted);">No data</div>`;
    return;
  }

  wrapper.innerHTML = arr.map(row => {
    const isPos    = row.change_pct >= 0;
    const initial  = (row.stock || "?").charAt(0);
    return `
      <div class="list-item">
        <div class="item-logo" style="background:${isPos ? "rgba(0,186,136,0.12)" : "rgba(248,81,73,0.1)"};color:${isPos ? "var(--positive)" : "var(--negative)"}">${escapeHtml(initial)}</div>
        <div class="item-info">
          <div class="item-title">${escapeHtml(row.stock)}</div>
          <div class="item-sub">NSE</div>
        </div>
        <div class="item-stats ms-auto text-end">
          <div class="item-val">${formatINR(row.close)}</div>
          <div class="item-pct ${isPos ? "pos" : "neg"} d-flex align-items-center gap-1 justify-content-end">
            <i class="fa-solid fa-arrow-trend-${isPos ? "up" : "down"}"></i>
            ${isPos ? "+" : ""}${row.change_pct.toFixed(2)}%
          </div>
        </div>
        <button class="add-btn ms-2" onclick="quickFetch('${escapeHtml(row.stock)}')" title="View chart">
          <i class="fa-solid fa-chart-bar"></i>
        </button>
      </div>`;
  }).join("");
}

// ================================================================
// 17. PORTFOLIO CHART (static demo)
// ================================================================
function initPortfolioChart() {
  const ctx = qs("#portfolio-chart");
  if (!ctx) return;
  new Chart(ctx.getContext("2d"), {
    type: "bar",
    data: {
      labels: ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul"],
      datasets: [
        { label: "2021", data: [200, 300, 450, 220, 250, 250, 300], backgroundColor: "#0A2523", borderRadius: 4, barPercentage: 0.6, categoryPercentage: 0.4 },
        { label: "2022", data: [280, 380, 500, 280, 480, 320, 380], backgroundColor: "#C4F60D", borderRadius: 4, barPercentage: 0.6, categoryPercentage: 0.4 }
      ]
    },
    options: {
      responsive: true, maintainAspectRatio: false,
      plugins: { legend: { display: false } },
      scales: {
        x: { grid: { display: false }, border: { display: false }, ticks: { font: { size: 10 } } },
        y: { grid: { color: "rgba(0,0,0,0.03)" }, position: "right", border: { display: false }, ticks: { font: { size: 10 }, stepSize: 100 } }
      }
    }
  });
}

// ================================================================
// 18. INIT
// ================================================================
document.addEventListener("DOMContentLoaded", () => {
  try {
    initTheme();
    initRouter();

    // Dashboard setup - wrap in try-catch to prevent initialization failures
    try { loadWatchlist().catch(e => console.warn("Watchlist load failed:", e)); } catch (e) { console.warn("Watchlist error:", e); }
    try { initPortfolioChart(); } catch (e) { console.warn("Portfolio chart error:", e); }
    try { fetchIndexQuickPicks().catch(e => console.warn("Quick picks load failed:", e)); } catch (e) { console.warn("Quick picks error:", e); }
    try { fetchGainersLosers().catch(e => console.warn("Gainers/losers load failed:", e)); } catch (e) { console.warn("Gainers/losers error:", e); }

    // Search on Enter key
    const symbolInput = qs("#symbol-input");
    if (symbolInput) {
      symbolInput.addEventListener("keydown", e => {
        if (e.key === "Enter") fetchStockData();
      });
    }

  // Search button
  const searchBtn = qs("#search-btn");
  if (searchBtn) searchBtn.addEventListener("click", fetchStockData);

  // Watchlist add on Enter
  const wlInput = qs("#wl-add-input");
  if (wlInput) {
    wlInput.addEventListener("keydown", e => {
      if (e.key === "Enter") addWatchlistItem();
    });
    // Clear error on typing
    wlInput.addEventListener("input", () => {
      qs("#wl-error").classList.remove("visible");
    });
  }

  // ML symbol inputs — Enter triggers predict
  const volInput   = qs("#vol-symbol");
  const priceInput = qs("#price-symbol");
  if (volInput)   volInput.addEventListener("keydown",   e => { if (e.key === "Enter") runVolatilityPredict(); });
  if (priceInput) priceInput.addEventListener("keydown", e => { if (e.key === "Enter") runPricePredict(); });

  console.log(`[BullLens] DEV_MODE=${DEV_MODE} | Theme: ${localStorage.getItem("bulllens_theme") || "light"}`);
  } catch (initError) {
    console.error("[BullLens] Initialization error:", initError);
    console.log("[BullLens] Page may be partially functional - buttons should still work");
  }
});

// ================================================================
// SETTINGS PANEL — navigation, save, theme picker
// ================================================================

/**
 * Switch the active settings panel (new st-* system).
 * @param {string} panelId  – ID of the target st-panel
 * @param {HTMLElement} btn – the clicked st-item button
 */
function stSwitch(panelId, btn) {
  document.querySelectorAll(".st-panel").forEach(p => p.classList.remove("active"));
  const target = document.getElementById(panelId);
  if (target) target.classList.add("active");
  document.querySelectorAll(".st-item").forEach(b => b.classList.remove("active"));
  if (btn) btn.classList.add("active");
}

/** @deprecated kept for backward compat */
function switchSettingsPanel(panelId, navItem) { stSwitch(panelId, navItem); }

/**
 * Show a settings-specific bottom-right toast.
 * @param {string} message
 * @param {boolean} [isError]
 */
function showSettingsToast(message, isError = false) {
  const toast = document.getElementById("st-toast");
  if (!toast) return;
  toast.innerHTML = `<i class="fa-solid fa-${isError ? "circle-exclamation" : "circle-check"}" style="color:${isError ? "var(--negative)" : "var(--accent)"}"></i> ${message}`;
  toast.classList.add("show");
  clearTimeout(toast._hideTimer);
  toast._hideTimer = setTimeout(() => toast.classList.remove("show"), 3000);
}

/**
 * Save a settings section to localStorage and show feedback.
 * In production you would POST to the relevant /api/* endpoint.
 * @param {string} section  – 'profile' | 'predictions' | 'market' | 'notifications' |
 *                            'appearance' | 'watchlist' | 'security' | 'feedback'
 */
async function saveSettings(section) {
  const stored = JSON.parse(localStorage.getItem("bl_settings") || "{}");

  switch (section) {
    case "profile":
      stored.profile = {
        name:     (document.getElementById("sp-name")     || {}).value || "",
        email:    (document.getElementById("sp-email")    || {}).value || "",
        bio:      (document.getElementById("sp-bio")      || {}).value || "",
        username: (document.getElementById("sp-username") || {}).value || "",
        phone:    (document.getElementById("sp-phone")    || {}).value || ""
      };
      break;

    case "predictions":
      stored.predictions = {
        type:       (document.getElementById("pp-type") || {}).value || "short-term",
        risk:       (document.getElementById("pp-risk") || {}).value || "medium",
        confidence: (document.getElementById("pp-conf") || {}).value || 70
      };
      break;

    case "market":
      stored.market = {
        primary: (document.getElementById("mk-primary") || {}).value || "NSE",
        nse:     document.getElementById("mk-nse")    && document.getElementById("mk-nse").classList.contains("active"),
        crypto:  document.getElementById("mk-crypto") && document.getElementById("mk-crypto").classList.contains("active"),
        us:      document.getElementById("mk-us")     && document.getElementById("mk-us").classList.contains("active")
      };
      break;

    case "notifications":
      stored.notifications = {
        channel: (document.getElementById("nt-channel") || {}).value || "push",
        buy:     document.getElementById("nt-buy")  && document.getElementById("nt-buy").classList.contains("active"),
        sell:    document.getElementById("nt-sell") && document.getElementById("nt-sell").classList.contains("active"),
        pred:    document.getElementById("nt-pred") && document.getElementById("nt-pred").classList.contains("active"),
        news:    document.getElementById("nt-news") && document.getElementById("nt-news").classList.contains("active")
      };
      break;

    case "appearance":
      stored.appearance = {
        theme:      stored.appearance ? stored.appearance.theme : "light",
        chartStyle: (document.getElementById("ap-chart")  || {}).value || "candlestick",
        grid:       document.getElementById("ap-grid")   && document.getElementById("ap-grid").classList.contains("active"),
        legend:     document.getElementById("ap-legend") && document.getElementById("ap-legend").classList.contains("active"),
        animations: document.getElementById("ap-anim")   && document.getElementById("ap-anim").classList.contains("active")
      };
      break;

    case "watchlist":
      stored.watchlist = {
        favs:    (document.getElementById("ws-favs")    || {}).value || "",
        sort:    (document.getElementById("ws-sort")    || {}).value || "alpha",
        refresh: (document.getElementById("ws-refresh") || {}).value || "60",
        price:   document.getElementById("ws-price") && document.getElementById("ws-price").classList.contains("active"),
        volume:  document.getElementById("ws-vol")   && document.getElementById("ws-vol").classList.contains("active")
      };
      break;

    case "security": {
      const newPwd     = (document.getElementById("sec-new")     || {}).value || "";
      const confirmPwd = (document.getElementById("sec-confirm") || {}).value || "";
      if (newPwd && newPwd !== confirmPwd) {
        showSettingsToast("Passwords do not match!", true);
        return;
      }
      stored.security = {
        twoFactor:      document.getElementById("sec-2fa")     && document.getElementById("sec-2fa").classList.contains("active"),
        sessionTimeout: document.getElementById("sec-timeout") && document.getElementById("sec-timeout").classList.contains("active")
      };
      break;
    }

    case "feedback": {
      const subject = (document.getElementById("hf-subject") || {}).value || "";
      const message = (document.getElementById("hf-message") || {}).value || "";
      if (!message.trim()) { showSettingsToast("Please enter a message before submitting.", true); return; }
      // Optionally POST to /api/feedback
      showSettingsToast("Feedback submitted — thank you! 🙏");
      if (document.getElementById("hf-subject")) document.getElementById("hf-subject").value = "";
      if (document.getElementById("hf-message")) document.getElementById("hf-message").value = "";
      return;
    }

    default:
      break;
  }

  localStorage.setItem("bl_settings", JSON.stringify(stored));

  const labels = {
    profile:       "Profile saved ✓",
    predictions:   "Prediction preferences saved ✓",
    market:        "Market selection saved ✓",
    notifications: "Notification settings saved ✓",
    appearance:    "Appearance settings saved ✓",
    watchlist:     "Watchlist settings saved ✓",
    security:      "Security settings updated ✓",
    feedback:      "Feedback submitted ✓"
  };
  showSettingsToast(labels[section] || "Settings saved ✓");
}

/**
 * Handle the visual theme picker (Light / Dark / Auto) in the Appearance panel.
 * Also applies the chosen theme immediately.
 * @param {'light'|'dark'|'auto'} choice
 */
function pickTheme(choice) {
  // Update picker UI
  ["light", "dark", "auto"].forEach(t => {
    const el = document.getElementById("th-" + t);
    if (el) el.classList.toggle("active", t === choice);
  });

  // Apply theme (treat 'auto' as system preference)
  let resolved = choice;
  if (choice === "auto") {
    resolved = window.matchMedia && window.matchMedia("(prefers-color-scheme: dark)").matches
      ? "dark" : "light";
  }
  const iconEl = document.getElementById("theme-icon");
  if (typeof setTheme === "function") setTheme(resolved, iconEl);

  // Persist choice
  const stored = JSON.parse(localStorage.getItem("bl_settings") || "{}");
  stored.appearance = { ...(stored.appearance || {}), theme: choice };
  localStorage.setItem("bl_settings", JSON.stringify(stored));
}

/** Restore saved settings into the settings form fields on page load */
function loadSavedSettings() {
  try {
    const stored = JSON.parse(localStorage.getItem("bl_settings") || "{}");

    // Profile
    if (stored.profile) {
      const set = (id, val) => { const el = document.getElementById(id); if (el) el.value = val || ""; };
      set("sp-name",     stored.profile.name);
      set("sp-email",    stored.profile.email);
      set("sp-bio",      stored.profile.bio);
      set("sp-username", stored.profile.username);
      set("sp-phone",    stored.profile.phone);
    }

    // Predictions
    if (stored.predictions) {
      const setV = (id, val) => { const el = document.getElementById(id); if (el) el.value = val; };
      setV("pp-type", stored.predictions.type);
      setV("pp-risk", stored.predictions.risk);
      const conf = document.getElementById("pp-conf");
      const confVal = document.getElementById("pp-conf-val");
      if (conf && stored.predictions.confidence) {
        conf.value = stored.predictions.confidence;
        if (confVal) confVal.textContent = stored.predictions.confidence + "%";
      }
    }

    // Market
    if (stored.market) {
      const setV = (id, val) => { const el = document.getElementById(id); if (el) el.value = val; };
      setV("mk-primary", stored.market.primary);
      const setT = (id, on) => { const el = document.getElementById(id); if (el) el.classList.toggle("active", !!on); };
      setT("mk-nse",    stored.market.nse);
      setT("mk-crypto", stored.market.crypto);
      setT("mk-us",     stored.market.us);
    }

    // Notifications
    if (stored.notifications) {
      const setV = (id, val) => { const el = document.getElementById(id); if (el) el.value = val; };
      setV("nt-channel", stored.notifications.channel);
      const setT = (id, on) => { const el = document.getElementById(id); if (el) el.classList.toggle("active", !!on); };
      setT("nt-buy",  stored.notifications.buy);
      setT("nt-sell", stored.notifications.sell);
      setT("nt-pred", stored.notifications.pred);
      setT("nt-news", stored.notifications.news);
    }

    // Appearance
    if (stored.appearance) {
      const setV = (id, val) => { const el = document.getElementById(id); if (el) el.value = val; };
      setV("ap-chart", stored.appearance.chartStyle);
      if (stored.appearance.theme) pickTheme(stored.appearance.theme);
    }

    // Watchlist
    if (stored.watchlist) {
      const setV = (id, val) => { const el = document.getElementById(id); if (el) el.value = val || ""; };
      setV("ws-favs",    stored.watchlist.favs);
      setV("ws-sort",    stored.watchlist.sort);
      setV("ws-refresh", stored.watchlist.refresh);
    }
  } catch (e) {
    console.warn("[BullLens] Could not restore settings:", e);
  }
}

// Auto-restore settings once DOM is ready
if (document.readyState === "loading") {
  document.addEventListener("DOMContentLoaded", loadSavedSettings);
} else {
  loadSavedSettings();
}
