"""Remove old settings CSS blocks and append new st-* CSS."""
import pathlib, re

CSS = pathlib.Path(r"c:\Users\ADMIN\OneDrive\Desktop\StockMarketPredictor\bulllens\static\css\style.css")
content = CSS.read_text(encoding="utf-8")

# Remove the old large settings block (from the "SETTINGS VIEW" comment to end)
pattern = re.compile(r'/\*\s*={2,}\s*[\r\n]+\s*SETTINGS VIEW.*', re.DOTALL)
content = pattern.sub('', content).rstrip() + '\n'

NEW_CSS = """
/* ============================================================
   SETTINGS VIEW  — WhatsApp / Telegram-style
   ============================================================ */

/* Outer wrapper: sidebar + content side-by-side */
.st-wrap {
  display: grid;
  grid-template-columns: 300px 1fr;
  gap: 0;
  min-height: calc(100vh - 130px);
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: var(--radius-card);
  overflow: hidden;
  box-shadow: var(--shadow-card);
}

/* ── Sidebar ── */
.st-side {
  background: var(--surface);
  border-right: 1px solid var(--border);
  display: flex;
  flex-direction: column;
  padding: 0;
  overflow-y: auto;
}

/* User mini-card at top of sidebar */
.st-user-card {
  display: flex;
  align-items: center;
  gap: 0.85rem;
  padding: 1.1rem 1.1rem 1rem;
  background: var(--bg);
  border-bottom: 1px solid var(--border);
}

.st-user-avatar {
  width: 44px;
  height: 44px;
  border-radius: 50%;
  background: rgba(31,178,140,0.15);
  color: #1fb28c;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.4rem;
  flex-shrink: 0;
}

.st-user-meta { display: flex; flex-direction: column; }
.st-user-name { font-size: 0.95rem; font-weight: 700; color: var(--text); }
.st-user-tag  { font-size: 0.74rem; color: var(--text-muted); margin-top: 2px; }

.st-divider { height: 1px; background: var(--border); margin: 0; }

/* Nav list */
.st-nav {
  display: flex;
  flex-direction: column;
  gap: 0;
  padding: 0.4rem 0;
}

/* Each sidebar item */
.st-item {
  width: 100%;
  display: flex;
  align-items: center;
  gap: 0.85rem;
  padding: 0.72rem 1.1rem;
  border: none;
  border-left: 3px solid transparent;
  background: transparent;
  cursor: pointer;
  text-align: left;
  font-family: inherit;
  transition: background 0.16s ease, border-color 0.16s ease;
  color: var(--text);
}

.st-item:hover {
  background: rgba(31,178,140,0.06);
}

.st-item.active {
  background: rgba(31,178,140,0.10);
  border-left-color: var(--accent);
}

/* Coloured icon circle */
.st-icon {
  width: 38px;
  height: 38px;
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 0.95rem;
  flex-shrink: 0;
  transition: transform 0.15s ease;
}

.st-item:hover .st-icon { transform: scale(1.06); }

/* Text block */
.st-text {
  display: flex;
  flex-direction: column;
  min-width: 0;
  flex: 1;
}

.st-title {
  font-size: 0.88rem;
  font-weight: 600;
  color: var(--text);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.st-sub {
  font-size: 0.73rem;
  color: var(--text-muted);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  margin-top: 2px;
}

/* Chevron */
.st-arrow {
  font-size: 0.7rem;
  color: var(--text-muted);
  flex-shrink: 0;
  transition: transform 0.2s ease, color 0.2s ease;
}
.st-item.active .st-arrow { color: var(--accent); transform: translateX(2px); }

/* Logout button */
.st-logout {
  display: flex;
  align-items: center;
  gap: 0.7rem;
  padding: 0.8rem 1.1rem;
  border: none;
  background: transparent;
  color: var(--negative);
  font-family: inherit;
  font-size: 0.88rem;
  font-weight: 600;
  cursor: pointer;
  width: 100%;
  text-align: left;
  transition: background 0.16s ease;
  margin-top: auto;
}
.st-logout:hover { background: rgba(248,81,73,0.08); }
.st-logout i { font-size: 0.9rem; }

/* ── Content area ── */
.st-content {
  flex: 1;
  background: var(--bg);
  overflow-y: auto;
  position: relative;
}

/* Panel visibility */
.st-panel { display: none; padding: 2rem; animation: fadeIn 0.2s ease; max-width: 680px; }
.st-panel.active { display: block; }

/* Panel header */
.st-ph {
  display: flex;
  align-items: flex-start;
  gap: 1rem;
  margin-bottom: 1.75rem;
  padding-bottom: 1.25rem;
  border-bottom: 1px solid var(--border);
}

.st-ph-icon {
  width: 48px;
  height: 48px;
  border-radius: 14px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.25rem;
  flex-shrink: 0;
}

.st-ph-title {
  font-size: 1.2rem;
  font-weight: 700;
  margin: 0 0 4px;
  color: var(--text);
}

.st-ph-desc {
  font-size: 0.85rem;
  color: var(--text-muted);
  margin: 0;
}

/* Group label (section heading inside panel) */
.st-group-label {
  font-size: 0.7rem;
  font-weight: 700;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  color: var(--text-muted);
  margin: 1.5rem 0 0.6rem;
}

/* Two-column form grid */
.st-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1.1rem;
}

.st-field {
  display: flex;
  flex-direction: column;
  gap: 5px;
}

.st-full { grid-column: 1 / -1; }

.st-field label {
  font-size: 0.82rem;
  font-weight: 600;
  color: var(--text);
  display: flex;
  align-items: center;
  gap: 6px;
}

.st-opt {
  font-size: 0.7rem;
  font-weight: 400;
  color: var(--text-muted);
}

.st-field input,
.st-field select,
.st-field textarea {
  padding: 0.58rem 0.85rem;
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: 10px;
  color: var(--text);
  font-size: 0.875rem;
  font-family: inherit;
  outline: none;
  transition: border-color 0.18s, box-shadow 0.18s;
}

.st-field input:focus,
.st-field select:focus,
.st-field textarea:focus {
  border-color: var(--accent);
  box-shadow: 0 0 0 3px rgba(31,178,140,0.12);
}

.st-field textarea { resize: vertical; }

.st-field select {
  cursor: pointer;
  appearance: none;
  background-image: url("data:image/svg+xml;charset=UTF-8,%3csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='%2394a3b8' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3e%3cpolyline points='6 9 12 15 18 9'%3e%3c/polyline%3e%3c/svg%3e");
  background-repeat: no-repeat;
  background-position: right 10px center;
  background-size: 15px;
  padding-right: 30px;
}

/* Range slider */
.st-field input[type="range"] {
  padding: 0; height: 5px; border-radius: 3px;
  background: var(--border); cursor: pointer;
  -webkit-appearance: none; appearance: none;
  box-shadow: none; border: none;
}
.st-field input[type="range"]::-webkit-slider-thumb {
  -webkit-appearance: none;
  width: 17px; height: 17px; border-radius: 50%;
  background: var(--accent); cursor: pointer;
  box-shadow: 0 2px 6px rgba(31,178,140,0.4);
}
.st-field input[type="range"]::-moz-range-thumb {
  width: 17px; height: 17px; border-radius: 50%;
  background: var(--accent); border: none; cursor: pointer;
}

.st-badge {
  background: rgba(31,178,140,0.15);
  color: var(--accent);
  font-size: 0.76rem;
  font-weight: 700;
  padding: 1px 8px;
  border-radius: 999px;
}

.st-hint { font-size: 0.76rem; color: var(--text-muted); }

.st-range-row {
  display: flex;
  justify-content: space-between;
  font-size: 0.7rem;
  color: var(--text-muted);
  margin-top: 3px;
}

/* Toggle list */
.st-toggle-list { display: flex; flex-direction: column; gap: 3px; }

.st-trow {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0.75rem 1rem;
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: 12px;
  transition: background 0.15s;
}
.st-trow:hover { background: var(--bg); }

.st-tinfo {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  min-width: 0;
}

.st-ticon {
  width: 36px; height: 36px;
  border-radius: 10px;
  display: flex; align-items: center; justify-content: center;
  font-size: 0.88rem; flex-shrink: 0;
}

.st-tinfo div {
  display: flex; flex-direction: column; gap: 2px;
}
.st-tinfo strong { font-size: 0.86rem; font-weight: 600; color: var(--text); }
.st-tinfo span   { font-size: 0.75rem; color: var(--text-muted); }

/* Toggle switch */
.st-toggle {
  position: relative;
  width: 44px; height: 24px;
  background: var(--border);
  border-radius: 12px;
  cursor: pointer;
  transition: background 0.22s ease;
  flex-shrink: 0;
}
.st-toggle.active { background: var(--accent); }
.st-knob {
  position: absolute;
  width: 18px; height: 18px;
  background: white;
  border-radius: 50%;
  top: 3px; left: 3px;
  transition: transform 0.22s ease;
  box-shadow: 0 1px 3px rgba(0,0,0,0.2);
}
.st-toggle.active .st-knob { transform: translateX(20px); }

/* Theme picker */
.st-theme-row { display: flex; gap: 0.85rem; flex-wrap: wrap; }

.st-theme-card {
  display: flex; flex-direction: column; align-items: center; gap: 6px;
  cursor: pointer; user-select: none;
}
.st-theme-card span {
  font-size: 0.78rem; font-weight: 600; color: var(--text-muted);
  transition: color 0.15s;
}
.st-theme-card.active span { color: var(--accent); }

.st-theme-preview {
  width: 80px; height: 52px;
  border-radius: 10px;
  border: 2px solid var(--border);
  transition: border-color 0.15s, box-shadow 0.15s;
}
.st-theme-card.active .st-theme-preview {
  border-color: var(--accent);
  box-shadow: 0 0 0 3px rgba(31,178,140,0.18);
}

/* Help quick-links */
.st-help-links { display: flex; flex-direction: column; gap: 6px; }

.st-help-row {
  display: flex; align-items: center; gap: 0.85rem;
  padding: 0.85rem 1rem;
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: 12px;
  text-decoration: none;
  color: var(--text);
  transition: background 0.15s, border-color 0.15s;
}
.st-help-row:hover { background: var(--bg); border-color: var(--accent); }
.st-help-row div { display: flex; flex-direction: column; gap: 2px; flex: 1; min-width: 0; }
.st-help-row strong { font-size: 0.86rem; font-weight: 600; }
.st-help-row span   { font-size: 0.75rem; color: var(--text-muted); }

/* Action bar */
.st-foot {
  margin-top: 1.5rem;
  padding-top: 1.1rem;
  border-top: 1px solid var(--border);
  display: flex;
  justify-content: flex-end;
}

.st-save {
  display: inline-flex; align-items: center; gap: 6px;
  padding: 0.58rem 1.3rem;
  background: var(--accent);
  color: white;
  border: none; border-radius: 10px;
  font-family: inherit; font-size: 0.875rem; font-weight: 600;
  cursor: pointer;
  transition: opacity 0.15s, transform 0.15s, box-shadow 0.15s;
  box-shadow: 0 4px 12px rgba(31,178,140,0.3);
}
.st-save:hover { opacity: 0.9; transform: translateY(-1px); box-shadow: 0 6px 16px rgba(31,178,140,0.4); }

/* Toast */
.st-toast {
  position: fixed; bottom: 1.5rem; right: 1.5rem; z-index: 9999;
  background: var(--surface);
  border: 1px solid var(--border);
  border-left: 4px solid var(--accent);
  border-radius: 12px;
  padding: 0.8rem 1.2rem;
  font-size: 0.875rem; font-weight: 600;
  color: var(--text);
  box-shadow: 0 8px 24px rgba(0,0,0,0.15);
  display: none; align-items: center; gap: 8px;
  max-width: 300px;
  animation: slideInToast 0.3s ease;
}
.st-toast.show { display: flex; }
@keyframes slideInToast {
  from { opacity:0; transform:translateY(12px); }
  to   { opacity:1; transform:translateY(0); }
}

/* Dark-mode tweaks */
[data-theme="dark"] .st-side { background: #131e2b; border-right-color: var(--border); }
[data-theme="dark"] .st-user-card { background: #0f1923; }
[data-theme="dark"] .st-trow,
[data-theme="dark"] .st-help-row { background: rgba(255,255,255,0.03); }
[data-theme="dark"] .st-trow:hover,
[data-theme="dark"] .st-help-row:hover { background: rgba(255,255,255,0.06); }
[data-theme="dark"] .st-field input,
[data-theme="dark"] .st-field select,
[data-theme="dark"] .st-field textarea { background: rgba(255,255,255,0.04); }

/* Responsive */
@media (max-width: 860px) {
  .st-wrap { grid-template-columns: 1fr; }
  .st-side { border-right: none; border-bottom: 1px solid var(--border); }
  .st-panel { padding: 1.25rem; }
  .st-grid { grid-template-columns: 1fr; }
  .st-full { grid-column: 1; }
  .st-side .st-logout { margin-top: 0; }
}
@media (max-width: 480px) {
  .st-theme-row { flex-wrap: wrap; }
  .st-theme-preview { width: 64px; height: 42px; }
}
"""

content += NEW_CSS
CSS.write_text(content, encoding="utf-8")
print("CSS updated.")
