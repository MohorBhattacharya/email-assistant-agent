"""
Email Assistant Agent — Streamlit App
Perceive → Decide → Act agent loop using Groq API (llama-3.3-70b-versatile)
"""

import streamlit as st
from groq import Groq
import json
from datetime import datetime

st.set_page_config(
    page_title="Mail Agent",
    page_icon="✉",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600&family=DM+Serif+Display&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

/* Hide default streamlit chrome */
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 0 !important; max-width: 100% !important; }
section[data-testid="stSidebar"] { background: #0f0f0f; border-right: 1px solid #1e1e1e; }
section[data-testid="stSidebar"] > div { padding: 0; }

/* Sidebar content */
.sb-header {
    padding: 28px 20px 20px;
    border-bottom: 1px solid #1e1e1e;
}
.sb-logo {
    font-family: 'DM Serif Display', serif;
    font-size: 22px;
    color: #ffffff;
    letter-spacing: -0.5px;
}
.sb-tagline {
    font-size: 11px;
    color: #555;
    margin-top: 3px;
    letter-spacing: 0.5px;
    text-transform: uppercase;
}
.sb-section { padding: 16px 20px; border-bottom: 1px solid #1a1a1a; }
.sb-section-title {
    font-size: 10px;
    font-weight: 600;
    letter-spacing: 1.2px;
    text-transform: uppercase;
    color: #444;
    margin-bottom: 10px;
}

/* Stat pills */
.stats-row { display: flex; gap: 8px; }
.stat-pill {
    flex: 1;
    text-align: center;
    padding: 8px 4px;
    border-radius: 8px;
    font-size: 11px;
    font-weight: 600;
}
.stat-urgent { background: #1a0a0a; color: #f87171; border: 1px solid #2d1111; }
.stat-action { background: #1a130a; color: #fbbf24; border: 1px solid #2d1f0a; }
.stat-info   { background: #0a0f1a; color: #60a5fa; border: 1px solid #0a1a2d; }

/* Email items in sidebar */
.email-item {
    padding: 12px 20px;
    cursor: pointer;
    border-bottom: 1px solid #141414;
    transition: background 0.15s;
}
.email-item:hover { background: #161616; }
.email-item.active { background: #1a1a1a; border-left: 2px solid #6366f1; }
.ei-row1 { display: flex; justify-content: space-between; align-items: center; margin-bottom: 3px; }
.ei-name { font-size: 13px; font-weight: 500; color: #e0e0e0; }
.ei-name.unread { color: #ffffff; font-weight: 600; }
.ei-time { font-size: 10px; color: #444; }
.ei-subject { font-size: 11px; color: #555; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; max-width: 190px; }
.ei-subject.unread { color: #888; }

/* Category badges */
.badge {
    display: inline-flex; align-items: center; gap: 4px;
    padding: 2px 8px; border-radius: 20px;
    font-size: 10px; font-weight: 600; letter-spacing: 0.3px;
}
.badge-urgent  { background: #1a0a0a; color: #f87171; border: 1px solid #2d1111; }
.badge-action  { background: #1a130a; color: #fbbf24; border: 1px solid #2d1f0a; }
.badge-info    { background: #0a0f1a; color: #60a5fa; border: 1px solid #0a1a2d; }
.badge-low     { background: #111; color: #666; border: 1px solid #1e1e1e; }
.badge-spam    { background: #111; color: #555; border: 1px solid #1e1e1e; }
.badge-new     { background: #13131a; color: #818cf8; border: 1px solid #1e1e2d; }

/* Main panel */
.main-wrap { padding: 0; height: 100vh; display: flex; flex-direction: column; background: #0a0a0a; }

/* Email header */
.email-header {
    padding: 28px 40px 20px;
    border-bottom: 1px solid #1a1a1a;
    background: #0d0d0d;
}
.email-subject-title {
    font-family: 'DM Serif Display', serif;
    font-size: 26px;
    color: #f0f0f0;
    letter-spacing: -0.5px;
    margin-bottom: 6px;
    line-height: 1.2;
}
.email-meta-row { display: flex; align-items: center; gap: 12px; flex-wrap: wrap; }
.email-from { font-size: 13px; color: #666; }
.email-from span { color: #999; }

/* Email body */
.email-body-wrap {
    padding: 28px 40px;
    background: #0a0a0a;
    border-bottom: 1px solid #1a1a1a;
}
.email-body-text {
    font-size: 14px;
    line-height: 1.8;
    color: #aaa;
    white-space: pre-wrap;
    max-width: 680px;
}

/* Analysis section */
.analysis-wrap { padding: 24px 40px; background: #0a0a0a; }
.section-label {
    font-size: 10px;
    font-weight: 600;
    letter-spacing: 1.5px;
    text-transform: uppercase;
    color: #333;
    margin-bottom: 16px;
}
.metrics-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 12px; margin-bottom: 20px; }
.metric-card {
    background: #0f0f0f;
    border: 1px solid #1a1a1a;
    border-radius: 10px;
    padding: 14px 16px;
}
.metric-label { font-size: 10px; color: #444; letter-spacing: 0.8px; text-transform: uppercase; margin-bottom: 6px; }
.metric-value { font-size: 15px; font-weight: 600; color: #e0e0e0; }
.metric-value.urgent  { color: #f87171; }
.metric-value.high    { color: #fbbf24; }
.metric-value.medium  { color: #60a5fa; }
.metric-value.low     { color: #666; }

.summary-card {
    background: #0f0f0f;
    border: 1px solid #1a1a1a;
    border-radius: 10px;
    padding: 16px 18px;
    margin-bottom: 16px;
}
.summary-text { font-size: 13px; color: #888; line-height: 1.7; }

.actions-list { margin-bottom: 20px; }
.action-item {
    display: flex; align-items: flex-start; gap: 10px;
    padding: 8px 0;
    border-bottom: 1px solid #141414;
    font-size: 13px; color: #777;
}
.action-arrow { color: #6366f1; font-size: 12px; margin-top: 1px; flex-shrink: 0; }

/* Reply section */
.reply-wrap { padding: 0 40px 32px; background: #0a0a0a; }
.reply-card {
    background: #0f0f0f;
    border: 1px solid #1e1e1e;
    border-radius: 12px;
    padding: 18px 20px;
}

/* Streamlit overrides */
div[data-testid="stTextArea"] textarea {
    background: #0f0f0f !important;
    border: 1px solid #1e1e1e !important;
    border-radius: 8px !important;
    color: #aaa !important;
    font-size: 13px !important;
    line-height: 1.7 !important;
    font-family: 'Inter', sans-serif !important;
}
div[data-testid="stTextInput"] input {
    background: #161616 !important;
    border: 1px solid #222 !important;
    color: #ccc !important;
    font-size: 13px !important;
    border-radius: 8px !important;
}
div[data-testid="stTextInput"] input::placeholder { color: #444 !important; }

/* Buttons */
div[data-testid="stButton"] > button {
    background: #6366f1 !important;
    color: white !important;
    border: none !important;
    border-radius: 8px !important;
    font-size: 13px !important;
    font-weight: 500 !important;
    padding: 10px 20px !important;
    transition: opacity 0.15s !important;
    width: 100%;
}
div[data-testid="stButton"] > button:hover { opacity: 0.85 !important; }

/* Secondary buttons */
button[kind="secondary"] {
    background: #161616 !important;
    color: #888 !important;
    border: 1px solid #222 !important;
}

.stSpinner > div { border-top-color: #6366f1 !important; }

div[data-testid="stExpander"] {
    background: #0f0f0f !important;
    border: 1px solid #1a1a1a !important;
    border-radius: 8px !important;
}

/* Memory log */
.memory-item {
    padding: 6px 0;
    border-bottom: 1px solid #141414;
    font-size: 11px;
    color: #555;
    font-family: 'Courier New', monospace;
}
.memory-item span { color: #6366f1; }

/* Empty state */
.empty-state {
    display: flex; flex-direction: column; align-items: center; justify-content: center;
    height: 70vh; color: #333; text-align: center;
}
.empty-icon { font-size: 48px; margin-bottom: 16px; }
.empty-title { font-family: 'DM Serif Display', serif; font-size: 22px; color: #444; margin-bottom: 8px; }
.empty-sub { font-size: 13px; color: #333; }

/* Warning/info overrides */
div[data-testid="stAlert"] {
    background: #0f0f13 !important;
    border: 1px solid #1e1e2d !important;
    border-radius: 8px !important;
    color: #818cf8 !important;
}
</style>
""", unsafe_allow_html=True)

# ── Data ──────────────────────────────────────────────────────────────────────
SAMPLE_EMAILS = [
    {
        "id": "e1", "from": "sarah.chen@client.com", "from_name": "Sarah Chen",
        "subject": "URGENT: Production server down", "time": "9:42 AM", "read": False,
        "body": "Hi,\n\nOur production server has been down for the past 2 hours and we're losing thousands of dollars per minute. This is a critical situation that needs immediate attention.\n\nI've tried reaching your on-call team but no one has responded. Can you please escalate this right now?\n\nThis is completely unacceptable.\n\nSarah Chen\nCTO, Acme Corp",
    },
    {
        "id": "e2", "from": "newsletters@medium.com", "from_name": "Medium Newsletter",
        "subject": "Top stories in AI this week", "time": "8:15 AM", "read": False,
        "body": "Hello,\n\nHere are this week's top AI stories curated just for you:\n\n1. GPT-5 rumored for Q3 release\n2. New breakthroughs in protein folding\n3. EU AI Act enforcement begins\n\nClick to read more on Medium.\n\n— The Medium Team",
    },
    {
        "id": "e3", "from": "james@partner.io", "from_name": "James Okoye",
        "subject": "Q3 proposal — need your review", "time": "Yesterday", "read": True,
        "body": "Hey,\n\nI've attached our Q3 partnership proposal. We'd love to get your team's feedback before we finalize next Friday.\n\nKey asks:\n- Review pricing section (pages 4-7)\n- Confirm the integration timeline works for your eng team\n- Legal sign-off on section 3.2\n\nLet me know if you need a call to walk through it.\n\nBest,\nJames",
    },
    {
        "id": "e4", "from": "hr@company.com", "from_name": "HR Team",
        "subject": "Reminder: Submit your timesheet by 5pm", "time": "Yesterday", "read": True,
        "body": "Hi team,\n\nJust a reminder to submit your timesheets for the week by 5:00 PM today. Late submissions may affect payroll processing.\n\nSubmit here: [timesheet portal link]\n\nThanks,\nHR Team",
    },
]

CATEGORY_CONFIG = {
    "urgent":          ("🔴", "Urgent",          "badge-urgent",  "urgent"),
    "action_required": ("🟡", "Action Required", "badge-action",  "high"),
    "informational":   ("🔵", "Informational",   "badge-info",    "medium"),
    "low_priority":    ("⚪", "Low Priority",    "badge-low",     "low"),
    "spam":            ("🗑", "Spam",            "badge-spam",    "low"),
}

PRIORITY_CLASS = {
    "1 - critical": "urgent",
    "2 - high": "high",
    "3 - medium": "medium",
    "4 - low": "low",
}

GROQ_MODEL = "llama-3.3-70b-versatile"

# ── Session state ─────────────────────────────────────────────────────────────
for k, v in [("emails", SAMPLE_EMAILS.copy()), ("analyses", {}),
              ("replies", {}), ("selected_id", None), ("memory", [])]:
    if k not in st.session_state:
        st.session_state[k] = v

# ── Agent ─────────────────────────────────────────────────────────────────────
def run_agent(email, api_key):
    client = Groq(api_key=api_key)
    system = """You are an intelligent email assistant agent (Perceive → Decide → Act).
Return ONLY raw valid JSON, no markdown, no explanation:
{
  "category": "urgent|action_required|informational|low_priority|spam",
  "priority": "1 - critical|2 - high|3 - medium|4 - low",
  "sentiment": "frustrated|positive|neutral|demanding|friendly|professional",
  "summary": "2-3 sentence summary of the email and what the sender needs.",
  "action_items": ["action 1", "action 2"],
  "reply": "Professional draft reply. Concise and warm. Body only, no subject."
}"""
    resp = client.chat.completions.create(
        model=GROQ_MODEL,
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": f"From: {email['from']}\nSubject: {email['subject']}\n\n{email['body']}"},
        ],
        temperature=0.3, max_tokens=1000,
    )
    raw = resp.choices[0].message.content.strip().replace("```json","").replace("```","").strip()
    result = json.loads(raw)
    st.session_state.memory.append({
        "ts": datetime.now().strftime("%H:%M:%S"),
        "subject": email["subject"][:22],
        "decision": result["category"],
        "priority": result["priority"],
    })
    return result

def regenerate_reply(email, api_key):
    client = Groq(api_key=api_key)
    resp = client.chat.completions.create(
        model=GROQ_MODEL,
        messages=[{"role": "user", "content":
            f"Write a professional email reply. Return ONLY the body.\n\nFrom: {email['from']}\nSubject: {email['subject']}\n\n{email['body']}"}],
        temperature=0.6, max_tokens=500,
    )
    return resp.choices[0].message.content.strip()

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div class="sb-header">
        <div class="sb-logo">✉ Mail Agent</div>
        <div class="sb-tagline">Groq · Llama 3.3 · AI-Powered</div>
    </div>
    """, unsafe_allow_html=True)

    # API Key
    st.markdown('<div class="sb-section">', unsafe_allow_html=True)
    st.markdown('<div class="sb-section-title">API Key</div>', unsafe_allow_html=True)
    api_key = st.text_input("", type="password", placeholder="gsk_...", label_visibility="collapsed")
    st.markdown('</div>', unsafe_allow_html=True)

    # Stats
    analyses = st.session_state.analyses
    n_u = sum(1 for a in analyses.values() if a.get("category") == "urgent")
    n_a = sum(1 for a in analyses.values() if a.get("category") == "action_required")
    n_i = sum(1 for a in analyses.values() if a.get("category") == "informational")
    st.markdown(f"""
    <div class="sb-section">
        <div class="sb-section-title">Overview</div>
        <div class="stats-row">
            <div class="stat-pill stat-urgent">🔴 {n_u}<br><span style="font-weight:400;font-size:9px;">urgent</span></div>
            <div class="stat-pill stat-action">🟡 {n_a}<br><span style="font-weight:400;font-size:9px;">action</span></div>
            <div class="stat-pill stat-info">🔵 {n_i}<br><span style="font-weight:400;font-size:9px;">info</span></div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Inbox list
    st.markdown('<div class="sb-section-title" style="padding: 16px 20px 0;">Inbox</div>', unsafe_allow_html=True)
    sorted_emails = sorted(
        st.session_state.emails,
        key=lambda e: {"urgent":0,"action_required":1,"informational":2,"low_priority":3,"spam":4}
                      .get(analyses.get(e["id"],{}).get("category",""), 5)
    )
    for em in sorted_emails:
        an = analyses.get(em["id"])
        if an:
            icon, label, badge_cls, _ = CATEGORY_CONFIG.get(an["category"], ("⚪","Low","badge-low","low"))
            badge = f'<span class="badge {badge_cls}">{icon} {label}</span>'
        else:
            badge = f'<span class="badge badge-new">{"● New" if not em["read"] else "—"}</span>'

        is_active = em["id"] == st.session_state.selected_id
        name_cls = "unread" if not em["read"] else ""
        subj_cls = "unread" if not em["read"] else ""

        st.markdown(f"""
        <div class="email-item {'active' if is_active else ''}">
            <div class="ei-row1">
                <span class="ei-name {name_cls}">{em['from_name']}</span>
                <span class="ei-time">{em['time']}</span>
            </div>
            <div class="ei-subject {subj_cls}">{em['subject']}</div>
            <div style="margin-top:5px;">{badge}</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button(f"Open", key=f"btn_{em['id']}", use_container_width=True):
            st.session_state.selected_id = em["id"]
            em["read"] = True
            st.rerun()

    # Add email
    st.markdown('<div style="padding: 12px 20px;">', unsafe_allow_html=True)
    with st.expander("＋ Add email"):
        nf = st.text_input("From", placeholder="sender@example.com", key="nf")
        ns = st.text_input("Subject", key="ns")
        nb = st.text_area("Body", key="nb", height=80)
        if st.button("Add to inbox", key="add_btn"):
            if nf and ns and nb:
                st.session_state.emails.insert(0, {
                    "id": f"c{len(st.session_state.emails)}",
                    "from": nf, "from_name": nf.split("@")[0],
                    "subject": ns, "time": datetime.now().strftime("%H:%M"),
                    "body": nb, "read": False,
                })
                st.session_state.selected_id = st.session_state.emails[0]["id"]
                st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

    # Memory
    if st.session_state.memory:
        st.markdown('<div class="sb-section">', unsafe_allow_html=True)
        st.markdown('<div class="sb-section-title">Agent Memory</div>', unsafe_allow_html=True)
        for m in reversed(st.session_state.memory[-5:]):
            st.markdown(f'<div class="memory-item"><span>{m["ts"]}</span> {m["subject"]}… → {m["decision"]}</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

# ── Main panel ────────────────────────────────────────────────────────────────
if not st.session_state.selected_id:
    st.markdown("""
    <div class="empty-state">
        <div class="empty-icon">✉</div>
        <div class="empty-title">Select an email to begin</div>
        <div class="empty-sub">The agent will classify, prioritize, and draft a reply for you.</div>
    </div>
    """, unsafe_allow_html=True)
else:
    email = next((e for e in st.session_state.emails if e["id"] == st.session_state.selected_id), None)
    if email:
        an = analyses.get(email["id"])

        # Badge for header
        if an:
            icon, label, badge_cls, _ = CATEGORY_CONFIG.get(an["category"], ("⚪","—","badge-low","low"))
            hdr_badge = f'<span class="badge {badge_cls}" style="font-size:11px;">{icon} {label}</span>'
        else:
            hdr_badge = ""

        # Email header
        st.markdown(f"""
        <div class="email-header">
            <div class="email-subject-title">{email['subject']}</div>
            <div class="email-meta-row">
                <span class="email-from">From: <span>{email['from']}</span></span>
                <span class="email-from">·</span>
                <span class="email-from">{email['time']}</span>
                {hdr_badge}
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Analyze button row
        col_space, col_btn = st.columns([3, 1])
        with col_btn:
            if not api_key:
                st.markdown('<div style="padding:8px 40px;"><small style="color:#444;">Enter API key →</small></div>', unsafe_allow_html=True)
            else:
                btn_label = "↺ Re-analyze" if an else "✦ Analyze & Draft Reply"
                if st.button(btn_label, key="analyze_btn"):
                    with st.spinner("Agent thinking..."):
                        try:
                            result = run_agent(email, api_key)
                            st.session_state.analyses[email["id"]] = result
                            st.session_state.replies[email["id"]] = result.get("reply", "")
                            st.rerun()
                        except Exception as ex:
                            st.error(f"Error: {ex}")

        # Email body
        st.markdown(f"""
        <div class="email-body-wrap">
            <div class="section-label">Message</div>
            <div class="email-body-text">{email['body']}</div>
        </div>
        """, unsafe_allow_html=True)

        # Analysis
        if an:
            pri = an.get("priority","—")
            pri_cls = PRIORITY_CLASS.get(pri, "low")
            cat = an.get("category","—").replace("_"," ").title()
            sent = an.get("sentiment","—").title()

            st.markdown(f"""
            <div class="analysis-wrap">
                <div class="section-label">Agent Analysis</div>
                <div class="metrics-grid">
                    <div class="metric-card">
                        <div class="metric-label">Category</div>
                        <div class="metric-value {pri_cls}">{cat}</div>
                    </div>
                    <div class="metric-card">
                        <div class="metric-label">Priority</div>
                        <div class="metric-value {pri_cls}">{pri}</div>
                    </div>
                    <div class="metric-card">
                        <div class="metric-label">Sentiment</div>
                        <div class="metric-value">{sent}</div>
                    </div>
                </div>
                <div class="summary-card">
                    <div class="metric-label" style="margin-bottom:8px;">Summary</div>
                    <div class="summary-text">{an.get('summary','')}</div>
                </div>
            """, unsafe_allow_html=True)

            items = an.get("action_items", [])
            if items:
                st.markdown('<div class="metric-label" style="margin-bottom:8px;">Suggested Actions</div>', unsafe_allow_html=True)
                actions_html = "".join(
                    f'<div class="action-item"><span class="action-arrow">→</span>{item}</div>'
                    for item in items
                )
                st.markdown(f'<div class="actions-list">{actions_html}</div>', unsafe_allow_html=True)

            st.markdown('</div>', unsafe_allow_html=True)

            # Reply draft
            st.markdown('<div class="reply-wrap">', unsafe_allow_html=True)
            st.markdown('<div class="section-label">Draft Reply</div>', unsafe_allow_html=True)
            current = st.session_state.replies.get(email["id"], "")
            edited = st.text_area("", value=current, height=160,
                                  key=f"reply_{email['id']}", label_visibility="collapsed")
            st.session_state.replies[email["id"]] = edited

            c1, c2, c3 = st.columns([1, 1, 2])
            with c1:
                if st.button("📋 Copy", key=f"copy_{email['id']}"):
                    st.toast("Copied to clipboard!")
            with c2:
                if api_key and st.button("↺ Regenerate", key=f"regen_{email['id']}"):
                    with st.spinner("Rewriting..."):
                        try:
                            st.session_state.replies[email["id"]] = regenerate_reply(email, api_key)
                            st.rerun()
                        except Exception as ex:
                            st.error(str(ex))
            st.markdown('</div>', unsafe_allow_html=True)