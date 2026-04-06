"""Patch script – replaces the old view-settings block in index.html."""
import re, pathlib, sys

HTML = pathlib.Path(r"c:\Users\ADMIN\OneDrive\Desktop\StockMarketPredictor\bulllens\templates\index.html")
content = HTML.read_text(encoding="utf-8")

NEW_SETTINGS = r"""    <div id="view-settings" class="spa-view">
      <div class="st-wrap">

        <!-- SETTINGS SIDEBAR -->
        <aside class="st-side">

          <div class="st-user-card">
            <div class="st-user-avatar"><i class="fa-solid fa-circle-user"></i></div>
            <div class="st-user-meta">
              <div class="st-user-name" id="st-username-label">{{ username or 'demo_user' }}</div>
              <div class="st-user-tag">BullLens Member</div>
            </div>
          </div>

          <div class="st-divider"></div>

          <nav class="st-nav">
            <button class="st-item active" onclick="stSwitch('stp-profile',this)">
              <span class="st-icon" style="background:rgba(31,178,140,.14);color:#1fb28c;"><i class="fa-solid fa-circle-user"></i></span>
              <span class="st-text"><span class="st-title">Profile</span><span class="st-sub">Name, email, account info</span></span>
              <i class="fa-solid fa-chevron-right st-arrow"></i>
            </button>
            <button class="st-item" onclick="stSwitch('stp-predictions',this)">
              <span class="st-icon" style="background:rgba(99,102,241,.14);color:#818cf8;"><i class="fa-solid fa-brain"></i></span>
              <span class="st-text"><span class="st-title">Prediction Preferences</span><span class="st-sub">Prediction type, confidence level, risk level</span></span>
              <i class="fa-solid fa-chevron-right st-arrow"></i>
            </button>
            <button class="st-item" onclick="stSwitch('stp-market',this)">
              <span class="st-icon" style="background:rgba(59,130,246,.14);color:#60a5fa;"><i class="fa-solid fa-globe"></i></span>
              <span class="st-text"><span class="st-title">Market Selection</span><span class="st-sub">NSE, Crypto, US stocks</span></span>
              <i class="fa-solid fa-chevron-right st-arrow"></i>
            </button>
            <button class="st-item" onclick="stSwitch('stp-notifications',this)">
              <span class="st-icon" style="background:rgba(245,158,11,.14);color:#fbbf24;"><i class="fa-solid fa-bell"></i></span>
              <span class="st-text"><span class="st-title">Notifications</span><span class="st-sub">Buy/sell alerts, prediction alerts</span></span>
              <i class="fa-solid fa-chevron-right st-arrow"></i>
            </button>
            <button class="st-item" onclick="stSwitch('stp-appearance',this)">
              <span class="st-icon" style="background:rgba(168,85,247,.14);color:#c084fc;"><i class="fa-solid fa-palette"></i></span>
              <span class="st-text"><span class="st-title">Appearance</span><span class="st-sub">Theme, display, chart style</span></span>
              <i class="fa-solid fa-chevron-right st-arrow"></i>
            </button>
            <button class="st-item" onclick="stSwitch('stp-watchlist',this)">
              <span class="st-icon" style="background:rgba(234,179,8,.14);color:#facc15;"><i class="fa-solid fa-star"></i></span>
              <span class="st-text"><span class="st-title">Watchlist Settings</span><span class="st-sub">Favorite stocks, tracking</span></span>
              <i class="fa-solid fa-chevron-right st-arrow"></i>
            </button>
            <button class="st-item" onclick="stSwitch('stp-security',this)">
              <span class="st-icon" style="background:rgba(16,185,129,.14);color:#34d399;"><i class="fa-solid fa-shield-halved"></i></span>
              <span class="st-text"><span class="st-title">Privacy &amp; Security</span><span class="st-sub">Password, login protection</span></span>
              <i class="fa-solid fa-chevron-right st-arrow"></i>
            </button>
            <button class="st-item" onclick="stSwitch('stp-help',this)">
              <span class="st-icon" style="background:rgba(14,165,233,.14);color:#38bdf8;"><i class="fa-solid fa-circle-question"></i></span>
              <span class="st-text"><span class="st-title">Help &amp; Feedback</span><span class="st-sub">Help center, report issue</span></span>
              <i class="fa-solid fa-chevron-right st-arrow"></i>
            </button>
          </nav>

          <div class="st-divider"></div>
          <button class="st-logout" onclick="doLogout()"><i class="fa-solid fa-right-from-bracket"></i> Log out</button>
        </aside>

        <!-- CONTENT PANELS -->
        <div class="st-content">
          <div class="st-toast" id="st-toast"></div>

          <!-- 1. PROFILE -->
          <section class="st-panel active" id="stp-profile">
            <div class="st-ph">
              <span class="st-ph-icon" style="background:rgba(31,178,140,.14);color:#1fb28c;"><i class="fa-solid fa-circle-user"></i></span>
              <div><h2 class="st-ph-title">Profile</h2><p class="st-ph-desc">Manage your personal information and account details</p></div>
            </div>
            <div class="st-grid">
              <div class="st-field"><label>Full Name</label><input type="text" id="sp-name" placeholder="Enter your full name"></div>
              <div class="st-field"><label>Email Address</label><input type="email" id="sp-email" placeholder="Email"></div>
              <div class="st-field"><label>Username</label><input type="text" id="sp-username" placeholder="@username"></div>
              <div class="st-field"><label>Phone</label><input type="text" id="sp-phone" placeholder="+91 00000 00000"></div>
              <div class="st-field st-full"><label>Bio <span class="st-opt">optional</span></label><textarea id="sp-bio" rows="3" placeholder="Tell us about yourself…"></textarea></div>
            </div>
            <div class="st-foot"><button class="st-save" onclick="saveSettings('profile')"><i class="fa-solid fa-floppy-disk"></i> Save Profile</button></div>
          </section>

          <!-- 2. PREDICTION PREFERENCES -->
          <section class="st-panel" id="stp-predictions">
            <div class="st-ph">
              <span class="st-ph-icon" style="background:rgba(99,102,241,.14);color:#818cf8;"><i class="fa-solid fa-brain"></i></span>
              <div><h2 class="st-ph-title">Prediction Preferences</h2><p class="st-ph-desc">Customise how BullLens generates forecasts for you</p></div>
            </div>
            <div class="st-grid">
              <div class="st-field"><label>Prediction Type</label><select id="pp-type"><option value="intraday">Intraday</option><option value="short-term" selected>Short-term (1–7 days)</option><option value="long-term">Long-term (1–3 months)</option></select></div>
              <div class="st-field"><label>Risk Level</label><select id="pp-risk"><option value="low">Low — Conservative</option><option value="medium" selected>Medium — Balanced</option><option value="high">High — Aggressive</option></select></div>
              <div class="st-field st-full">
                <label>Confidence Threshold &nbsp;<span class="st-badge" id="pp-conf-val">70%</span></label>
                <small class="st-hint">Only show predictions above this confidence level</small>
                <input type="range" id="pp-conf" min="10" max="100" step="5" value="70" oninput="document.getElementById('pp-conf-val').textContent=this.value+'%'">
                <div class="st-range-row"><span>10%</span><span>100%</span></div>
              </div>
            </div>
            <div class="st-foot"><button class="st-save" onclick="saveSettings('predictions')"><i class="fa-solid fa-floppy-disk"></i> Save Preferences</button></div>
          </section>

          <!-- 3. MARKET SELECTION -->
          <section class="st-panel" id="stp-market">
            <div class="st-ph">
              <span class="st-ph-icon" style="background:rgba(59,130,246,.14);color:#60a5fa;"><i class="fa-solid fa-globe"></i></span>
              <div><h2 class="st-ph-title">Market Selection</h2><p class="st-ph-desc">Choose which markets appear in your dashboard</p></div>
            </div>
            <div class="st-grid">
              <div class="st-field"><label>Primary Market</label><select id="mk-primary"><option value="NSE" selected>NSE — Indian Stocks</option><option value="Crypto">Crypto</option><option value="US">US Stocks</option></select></div>
            </div>
            <p class="st-group-label">Enable / Disable Markets</p>
            <div class="st-toggle-list">
              <div class="st-trow"><div class="st-tinfo"><div class="st-ticon" style="background:rgba(31,178,140,.14);color:#1fb28c;"><i class="fa-solid fa-indian-rupee-sign"></i></div><div><strong>NSE</strong><span>Indian National Stock Exchange</span></div></div><div class="st-toggle active" id="mk-nse" onclick="this.classList.toggle('active')"><div class="st-knob"></div></div></div>
              <div class="st-trow"><div class="st-tinfo"><div class="st-ticon" style="background:rgba(245,158,11,.14);color:#f59e0b;"><i class="fa-brands fa-bitcoin"></i></div><div><strong>Crypto</strong><span>BTC, ETH and others</span></div></div><div class="st-toggle active" id="mk-crypto" onclick="this.classList.toggle('active')"><div class="st-knob"></div></div></div>
              <div class="st-trow"><div class="st-tinfo"><div class="st-ticon" style="background:rgba(59,130,246,.14);color:#3b82f6;"><i class="fa-solid fa-flag-usa"></i></div><div><strong>US Stocks</strong><span>NYSE, NASDAQ equities</span></div></div><div class="st-toggle" id="mk-us" onclick="this.classList.toggle('active')"><div class="st-knob"></div></div></div>
            </div>
            <div class="st-foot"><button class="st-save" onclick="saveSettings('market')"><i class="fa-solid fa-floppy-disk"></i> Save Markets</button></div>
          </section>

          <!-- 4. NOTIFICATIONS -->
          <section class="st-panel" id="stp-notifications">
            <div class="st-ph">
              <span class="st-ph-icon" style="background:rgba(245,158,11,.14);color:#fbbf24;"><i class="fa-solid fa-bell"></i></span>
              <div><h2 class="st-ph-title">Notifications</h2><p class="st-ph-desc">Control which alerts you receive and how</p></div>
            </div>
            <div class="st-grid">
              <div class="st-field"><label>Notification Channel</label><select id="nt-channel"><option value="email">Email</option><option value="push" selected>Push Notification</option><option value="sms">SMS</option><option value="all">All Channels</option></select></div>
            </div>
            <p class="st-group-label">Alert Types</p>
            <div class="st-toggle-list">
              <div class="st-trow"><div class="st-tinfo"><div class="st-ticon" style="background:rgba(16,185,129,.14);color:#10b981;"><i class="fa-solid fa-arrow-trend-up"></i></div><div><strong>Buy Alerts</strong><span>Notify me of buy signals</span></div></div><div class="st-toggle active" id="nt-buy" onclick="this.classList.toggle('active')"><div class="st-knob"></div></div></div>
              <div class="st-trow"><div class="st-tinfo"><div class="st-ticon" style="background:rgba(248,81,73,.14);color:#f85149;"><i class="fa-solid fa-arrow-trend-down"></i></div><div><strong>Sell Alerts</strong><span>Notify me of sell signals</span></div></div><div class="st-toggle active" id="nt-sell" onclick="this.classList.toggle('active')"><div class="st-knob"></div></div></div>
              <div class="st-trow"><div class="st-tinfo"><div class="st-ticon" style="background:rgba(139,92,246,.14);color:#8b5cf6;"><i class="fa-solid fa-wand-magic-sparkles"></i></div><div><strong>Prediction Alerts</strong><span>New ML prediction alerts</span></div></div><div class="st-toggle active" id="nt-pred" onclick="this.classList.toggle('active')"><div class="st-knob"></div></div></div>
              <div class="st-trow"><div class="st-tinfo"><div class="st-ticon" style="background:rgba(31,178,140,.14);color:#1fb28c;"><i class="fa-solid fa-newspaper"></i></div><div><strong>Market News</strong><span>Breaking news for your stocks</span></div></div><div class="st-toggle" id="nt-news" onclick="this.classList.toggle('active')"><div class="st-knob"></div></div></div>
            </div>
            <div class="st-foot"><button class="st-save" onclick="saveSettings('notifications')"><i class="fa-solid fa-floppy-disk"></i> Save Notifications</button></div>
          </section>

          <!-- 5. APPEARANCE -->
          <section class="st-panel" id="stp-appearance">
            <div class="st-ph">
              <span class="st-ph-icon" style="background:rgba(168,85,247,.14);color:#c084fc;"><i class="fa-solid fa-palette"></i></span>
              <div><h2 class="st-ph-title">Appearance</h2><p class="st-ph-desc">Personalise the look and feel of BullLens</p></div>
            </div>
            <p class="st-group-label">Theme</p>
            <div class="st-theme-row">
              <div class="st-theme-card active" id="th-light" onclick="pickTheme('light')"><div class="st-theme-preview" style="background:linear-gradient(135deg,#f6f8f9 55%,#fff 45%);"></div><span>Light</span></div>
              <div class="st-theme-card" id="th-dark" onclick="pickTheme('dark')"><div class="st-theme-preview" style="background:linear-gradient(135deg,#0f1923 55%,#1a2535 45%);"></div><span>Dark</span></div>
              <div class="st-theme-card" id="th-auto" onclick="pickTheme('auto')"><div class="st-theme-preview" style="background:linear-gradient(135deg,#f6f8f9 50%,#0f1923 50%);"></div><span>Auto</span></div>
            </div>
            <div class="st-grid" style="margin-top:1.25rem;">
              <div class="st-field"><label>Chart Style</label><select id="ap-chart"><option value="candlestick" selected>Candlestick</option><option value="line">Line</option><option value="area">Area</option><option value="bars">OHLC Bars</option></select></div>
            </div>
            <p class="st-group-label">Display Options</p>
            <div class="st-toggle-list">
              <div class="st-trow"><div class="st-tinfo"><div class="st-ticon" style="background:rgba(99,102,241,.14);color:#6366f1;"><i class="fa-solid fa-border-all"></i></div><div><strong>Show Grid Lines</strong><span>Display grid on charts</span></div></div><div class="st-toggle active" id="ap-grid" onclick="this.classList.toggle('active')"><div class="st-knob"></div></div></div>
              <div class="st-trow"><div class="st-tinfo"><div class="st-ticon" style="background:rgba(31,178,140,.14);color:#1fb28c;"><i class="fa-solid fa-tags"></i></div><div><strong>Show Legend</strong><span>Display chart legend</span></div></div><div class="st-toggle active" id="ap-legend" onclick="this.classList.toggle('active')"><div class="st-knob"></div></div></div>
            </div>
            <div class="st-foot"><button class="st-save" onclick="saveSettings('appearance')"><i class="fa-solid fa-floppy-disk"></i> Save Appearance</button></div>
          </section>

          <!-- 6. WATCHLIST -->
          <section class="st-panel" id="stp-watchlist">
            <div class="st-ph">
              <span class="st-ph-icon" style="background:rgba(234,179,8,.14);color:#facc15;"><i class="fa-solid fa-star"></i></span>
              <div><h2 class="st-ph-title">Watchlist Settings</h2><p class="st-ph-desc">Manage your favourite stocks and tracking preferences</p></div>
            </div>
            <div class="st-grid">
              <div class="st-field st-full"><label>Favourite Stocks <span class="st-opt">comma-separated</span></label><textarea id="ws-favs" rows="3" placeholder="e.g. TCS, INFY, RELIANCE, WIPRO"></textarea></div>
              <div class="st-field"><label>Default Sort</label><select id="ws-sort"><option value="alpha" selected>Alphabetical</option><option value="change">% Change</option><option value="price">Price</option></select></div>
              <div class="st-field"><label>Auto-Refresh</label><select id="ws-refresh"><option value="30">Every 30 sec</option><option value="60" selected>Every 1 min</option><option value="300">Every 5 min</option><option value="0">Manual only</option></select></div>
            </div>
            <p class="st-group-label">Tracking Options</p>
            <div class="st-toggle-list">
              <div class="st-trow"><div class="st-tinfo"><div class="st-ticon" style="background:rgba(16,185,129,.14);color:#10b981;"><i class="fa-solid fa-dollar-sign"></i></div><div><strong>Track Price Changes</strong><span>Monitor real-time movements</span></div></div><div class="st-toggle active" id="ws-price" onclick="this.classList.toggle('active')"><div class="st-knob"></div></div></div>
              <div class="st-trow"><div class="st-tinfo"><div class="st-ticon" style="background:rgba(59,130,246,.14);color:#3b82f6;"><i class="fa-solid fa-wave-square"></i></div><div><strong>Track Volume</strong><span>Monitor trading volume spikes</span></div></div><div class="st-toggle active" id="ws-vol" onclick="this.classList.toggle('active')"><div class="st-knob"></div></div></div>
            </div>
            <div class="st-foot"><button class="st-save" onclick="saveSettings('watchlist')"><i class="fa-solid fa-floppy-disk"></i> Save Settings</button></div>
          </section>

          <!-- 7. PRIVACY & SECURITY -->
          <section class="st-panel" id="stp-security">
            <div class="st-ph">
              <span class="st-ph-icon" style="background:rgba(16,185,129,.14);color:#34d399;"><i class="fa-solid fa-shield-halved"></i></span>
              <div><h2 class="st-ph-title">Privacy &amp; Security</h2><p class="st-ph-desc">Keep your account safe with a strong password</p></div>
            </div>
            <div class="st-grid">
              <div class="st-field st-full"><label>Current Password</label><input type="password" id="sec-cur" placeholder="Enter current password"></div>
              <div class="st-field"><label>New Password</label><input type="password" id="sec-new" placeholder="New password"></div>
              <div class="st-field"><label>Confirm Password</label><input type="password" id="sec-confirm" placeholder="Confirm password"></div>
            </div>
            <p class="st-group-label">Login Protection</p>
            <div class="st-toggle-list">
              <div class="st-trow"><div class="st-tinfo"><div class="st-ticon" style="background:rgba(139,92,246,.14);color:#8b5cf6;"><i class="fa-solid fa-mobile-screen"></i></div><div><strong>Two-Factor Authentication</strong><span>Require OTP on every login</span></div></div><div class="st-toggle" id="sec-2fa" onclick="this.classList.toggle('active')"><div class="st-knob"></div></div></div>
              <div class="st-trow"><div class="st-tinfo"><div class="st-ticon" style="background:rgba(31,178,140,.14);color:#1fb28c;"><i class="fa-solid fa-clock-rotate-left"></i></div><div><strong>Session Timeout</strong><span>Auto-logout after 30 min inactive</span></div></div><div class="st-toggle active" id="sec-timeout" onclick="this.classList.toggle('active')"><div class="st-knob"></div></div></div>
            </div>
            <div class="st-foot"><button class="st-save" onclick="saveSettings('security')"><i class="fa-solid fa-floppy-disk"></i> Update Password</button></div>
          </section>

          <!-- 8. HELP & FEEDBACK -->
          <section class="st-panel" id="stp-help">
            <div class="st-ph">
              <span class="st-ph-icon" style="background:rgba(14,165,233,.14);color:#38bdf8;"><i class="fa-solid fa-circle-question"></i></span>
              <div><h2 class="st-ph-title">Help &amp; Feedback</h2><p class="st-ph-desc">Browse the help centre or report an issue</p></div>
            </div>
            <div class="st-help-links">
              <a class="st-help-row" href="#" onclick="return false;"><div class="st-ticon" style="background:rgba(14,165,233,.14);color:#38bdf8;"><i class="fa-solid fa-book"></i></div><div><strong>Documentation</strong><span>Guides, tutorials and FAQs</span></div><i class="fa-solid fa-chevron-right" style="color:var(--text-muted);font-size:.75rem;margin-left:auto;"></i></a>
              <a class="st-help-row" href="#" onclick="return false;"><div class="st-ticon" style="background:rgba(248,81,73,.14);color:#f85149;"><i class="fa-solid fa-bug"></i></div><div><strong>Report a Bug</strong><span>Tell us what went wrong</span></div><i class="fa-solid fa-chevron-right" style="color:var(--text-muted);font-size:.75rem;margin-left:auto;"></i></a>
              <a class="st-help-row" href="#" onclick="return false;"><div class="st-ticon" style="background:rgba(234,179,8,.14);color:#facc15;"><i class="fa-solid fa-lightbulb"></i></div><div><strong>Feature Request</strong><span>Suggest something new</span></div><i class="fa-solid fa-chevron-right" style="color:var(--text-muted);font-size:.75rem;margin-left:auto;"></i></a>
            </div>
            <p class="st-group-label" style="margin-top:1.5rem;">Send Feedback</p>
            <div class="st-grid">
              <div class="st-field"><label>Issue Type</label><select id="hf-type"><option value="bug">Bug Report</option><option value="feature">Feature Suggestion</option><option value="feedback" selected>General Feedback</option><option value="other">Other</option></select></div>
              <div class="st-field"><label>Subject</label><input type="text" id="hf-subject" placeholder="Brief summary"></div>
              <div class="st-field st-full"><label>Message</label><textarea id="hf-message" rows="4" placeholder="Describe in detail…"></textarea></div>
            </div>
            <div class="st-foot"><button class="st-save" onclick="saveSettings('feedback')"><i class="fa-solid fa-paper-plane"></i> Submit Feedback</button></div>
          </section>

        </div><!-- /st-content -->
      </div><!-- /st-wrap -->
    </div><!-- /view-settings -->"""

# Match from the opening div to the closing comment
pattern = re.compile(
    r'<div id="view-settings" class="spa-view">.*?</div><!--\s*/view-settings\s*-->',
    re.DOTALL
)

if not pattern.search(content):
    print("ERROR: pattern not found"); sys.exit(1)

new_content = pattern.sub(NEW_SETTINGS, content, count=1)
HTML.write_text(new_content, encoding="utf-8")
print("Done — settings view patched successfully.")
