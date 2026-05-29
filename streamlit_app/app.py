"""
Email Assistant Agent — War Room Edition
Three AI agents debate how to respond to every email.
Agent Rex (aggressive) vs Agent Sage (diplomatic) vs Agent Nova (analytical)
Powered by Groq API (llama-3.3-70b-versatile)
"""

import streamlit as st
from groq import Groq
import json
from datetime import datetime

st.set_page_config(
    page_title="Mail Agent — War Room",
    page_icon="⚔",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600&family=DM+Serif+Display&display=swap');
html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 0 !important; max-width: 100% !important; }
section[data-testid="stSidebar"] { background: #0a0a0a; border-right: 1px solid #1a1a1a; }
section[data-testid="stSidebar"] > div { padding: 0; }
.sb-header { padding: 24px 20px 16px; border-bottom: 1px solid #1a1a1a; }
.sb-logo { font-family: 'DM Serif Display', serif; font-size: 20px; color: #fff; letter-spacing: -0.5px; }
.sb-tagline { font-size: 10px; color: #444; margin-top: 3px; letter-spacing: 1px; text-transform: uppercase; }
.sb-section { padding: 14px 20px; border-bottom: 1px solid #141414; }
.sb-section-title { font-size: 9px; font-weight: 600; letter-spacing: 1.5px; text-transform: uppercase; color: #383838; margin-bottom: 10px; }
.stats-row { display: flex; gap: 6px; }
.stat-pill { flex: 1; text-align: center; padding: 8px 4px; border-radius: 8px; font-size: 10px; font-weight: 600; line-height: 1.6; }
.stat-urgent { background: #1a0808; color: #f87171; border: 1px solid #2d1010; }
.stat-action { background: #1a1208; color: #fbbf24; border: 1px solid #2d1e08; }
.stat-info   { background: #080d1a; color: #60a5fa; border: 1px solid #08122d; }
.email-item { padding: 12px 20px; border-bottom: 1px solid #111; transition: background 0.12s; }
.email-item:hover { background: #111; }
.email-item.active { background: #131313; border-left: 2px solid #818cf8; }
.ei-top { display: flex; justify-content: space-between; align-items: center; margin-bottom: 3px; }
.ei-name { font-size: 12px; font-weight: 600; color: #ddd; }
.ei-name.unread { color: #fff; }
.ei-time { font-size: 10px; color: #383838; }
.ei-subject { font-size: 11px; color: #484848; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; max-width: 185px; margin-bottom: 5px; }
.ei-subject.unread { color: #777; }
.badge { display: inline-flex; align-items: center; gap: 3px; padding: 2px 7px; border-radius: 20px; font-size: 9px; font-weight: 700; letter-spacing: 0.4px; }
.badge-urgent { background: #1a0808; color: #f87171; border: 1px solid #2d1010; }
.badge-action { background: #1a1208; color: #fbbf24; border: 1px solid #2d1e08; }
.badge-info   { background: #080d1a; color: #60a5fa; border: 1px solid #08122d; }
.badge-low    { background: #111; color: #555; border: 1px solid #1e1e1e; }
.badge-spam   { background: #111; color: #444; border: 1px solid #1e1e1e; }
.badge-new    { background: #10101a; color: #818cf8; border: 1px solid #1a1a2d; }
.memory-item { padding: 5px 0; border-bottom: 1px solid #111; font-size: 10px; color: #444; font-family: monospace; }
.memory-item span { color: #818cf8; }
.main-bg { background: #080808; min-height: 100vh; }
.email-header { padding: 28px 36px 18px; border-bottom: 1px solid #141414; background: #0a0a0a; }
.email-title { font-family: 'DM Serif Display', serif; font-size: 24px; color: #f0f0f0; letter-spacing: -0.3px; margin-bottom: 6px; line-height: 1.2; }
.email-meta { display: flex; align-items: center; gap: 10px; font-size: 12px; color: #555; flex-wrap: wrap; }
.email-meta span { color: #888; }
.email-body-section { padding: 20px 36px; border-bottom: 1px solid #141414; background: #080808; }
.section-eyebrow { font-size: 9px; font-weight: 700; letter-spacing: 1.8px; text-transform: uppercase; color: #2e2e2e; margin-bottom: 10px; }
.email-body-text { font-size: 13px; line-height: 1.8; color: #888; white-space: pre-wrap; max-width: 640px; }
.warroom-section { padding: 24px 36px; background: #080808; }
.warroom-title { font-family: 'DM Serif Display', serif; font-size: 18px; color: #ccc; margin-bottom: 6px; }
.warroom-sub { font-size: 11px; color: #333; margin-bottom: 20px; }
.agents-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 14px; margin-bottom: 20px; }
.agent-card { border-radius: 12px; padding: 16px; border: 1px solid; position: relative; overflow: hidden; }
.agent-rex  { background: #120808; border-color: #2d1010; }
.agent-sage { background: #080d12; border-color: #08122d; }
.agent-nova { background: #0d1208; border-color: #122d08; }
.agent-header { display: flex; align-items: center; gap: 10px; margin-bottom: 12px; }
.agent-avatar { width: 38px; height: 38px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 18px; flex-shrink: 0; }
.avatar-rex  { background: #2d1010; }
.avatar-sage { background: #08122d; }
.avatar-nova { background: #122d08; }
.agent-name { font-size: 13px; font-weight: 700; }
.agent-name.rex  { color: #f87171; }
.agent-name.sage { color: #60a5fa; }
.agent-name.nova { color: #86efac; }
.agent-role { font-size: 9px; letter-spacing: 0.8px; text-transform: uppercase; color: #444; margin-top: 1px; }
.agent-stance { font-size: 11px; line-height: 1.65; color: #666; min-height: 60px; }
.agent-vote { margin-top: 10px; padding-top: 10px; border-top: 1px solid #1e1e1e; font-size: 10px; }
.vote-label { color: #333; letter-spacing: 0.5px; text-transform: uppercase; font-size: 9px; margin-bottom: 3px; }
.vote-text { font-size: 11px; font-weight: 600; }
.vote-rex  { color: #f87171; }
.vote-sage { color: #60a5fa; }
.vote-nova { color: #86efac; }
.debate-section { margin-bottom: 20px; }
.debate-title { font-size: 9px; font-weight: 700; letter-spacing: 1.8px; text-transform: uppercase; color: #2e2e2e; margin-bottom: 12px; }
.debate-bubble { display: flex; gap: 10px; margin-bottom: 10px; align-items: flex-start; }
.bubble-avatar { width: 26px; height: 26px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 12px; flex-shrink: 0; margin-top: 2px; }
.bubble-content { flex: 1; }
.bubble-name { font-size: 10px; font-weight: 700; margin-bottom: 3px; }
.bubble-name.rex  { color: #f87171; }
.bubble-name.sage { color: #60a5fa; }
.bubble-name.nova { color: #86efac; }
.bubble-text { font-size: 12px; line-height: 1.6; color: #666; background: #0f0f0f; border-radius: 0 8px 8px 8px; padding: 8px 12px; border: 1px solid #1a1a1a; }
.consensus-card { background: #0c0c10; border: 1px solid #1e1e2d; border-radius: 12px; padding: 18px 20px; margin-bottom: 16px; }
.consensus-header { display: flex; align-items: center; gap: 8px; margin-bottom: 12px; }
.consensus-icon { font-size: 16px; }
.consensus-label { font-size: 11px; font-weight: 700; color: #818cf8; letter-spacing: 0.5px; }
.consensus-verdict { font-size: 12px; color: #555; margin-bottom: 12px; font-style: italic; }
.reply-section { padding: 0 36px 32px; background: #080808; }
div[data-testid="stTextArea"] textarea {
    background: #0d0d0d !important; border: 1px solid #1e1e1e !important;
    border-radius: 8px !important; color: #999 !important;
    font-size: 13px !important; line-height: 1.7 !important;
    font-family: 'Inter', sans-serif !important;
}
div[data-testid="stTextInput"] input {
    background: #111 !important; border: 1px solid #1e1e1e !important;
    color: #ccc !important; font-size: 13px !important; border-radius: 8px !important;
}
div[data-testid="stButton"] > button {
    background: #818cf8 !important; color: #fff !important;
    border: none !important; border-radius: 8px !important;
    font-size: 13px !important; font-weight: 600 !important;
    padding: 10px 20px !important; width: 100% !important;
    transition: opacity 0.15s !important;
}
div[data-testid="stButton"] > button:hover { opacity: 0.85 !important; }
div[data-testid="stExpander"] {
    background: #0d0d0d !important; border: 1px solid #1a1a1a !important; border-radius: 8px !important;
}
.empty-state { display: flex; flex-direction: column; align-items: center; justify-content: center; height: 75vh; text-align: center; }
.empty-icon { font-size: 44px; margin-bottom: 14px; }
.empty-title { font-family: 'DM Serif Display', serif; font-size: 22px; color: #333; margin-bottom: 8px; }
.empty-sub { font-size: 12px; color: #2a2a2a; max-width: 300px; line-height: 1.6; }
</style>
""", unsafe_allow_html=True)

# ── Config ────────────────────────────────────────────────────────────────────
GROQ_API_KEY = "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"   
GROQ_MODEL   = "llama-3.3-70b-versatile"

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
    "urgent":          ("🔴", "Urgent",  "badge-urgent"),
    "action_required": ("🟡", "Action",  "badge-action"),
    "informational":   ("🔵", "Info",    "badge-info"),
    "low_priority":    ("⚪", "Low",     "badge-low"),
    "spam":            ("🗑", "Spam",    "badge-spam"),
}

AGENTS = {
    "rex":  {"name": "Rex",  "emoji": "🔴", "avatar_cls": "avatar-rex",  "card_cls": "agent-rex",  "name_cls": "rex",  "role": "Aggressive · Direct"},
    "sage": {"name": "Sage", "emoji": "🔵", "avatar_cls": "avatar-sage", "card_cls": "agent-sage", "name_cls": "sage", "role": "Diplomatic · Empathetic"},
    "nova": {"name": "Nova", "emoji": "🟢", "avatar_cls": "avatar-nova", "card_cls": "agent-nova", "name_cls": "nova", "role": "Analytical · Strategic"},
}

# ── Session state ─────────────────────────────────────────────────────────────
for k, v in [("emails", SAMPLE_EMAILS.copy()), ("debates", {}),
              ("selected_id", None), ("memory", [])]:
    if k not in st.session_state:
        st.session_state[k] = v

# ── Agent functions ───────────────────────────────────────────────────────────
def call_agent(client, agent_id, email, context=""):
    personas = {
        "rex":  "You are Agent Rex — aggressive, blunt, results-focused. You believe in direct confrontation and urgent action. You don't sugarcoat anything. Your tone is firm and commanding.",
        "sage": "You are Agent Sage — empathetic, diplomatic, relationship-first. You believe every interaction is a chance to strengthen the relationship. Your tone is warm, professional, and measured.",
        "nova": "You are Agent Nova — analytical, data-driven, systematic. You break problems into components and evaluate options. Your tone is precise and objective.",
    }
    debate_context = f"\n\nOther agents have said:\n{context}" if context else ""
    prompt = f"""Analyze this email and give your response as {agent_id.upper()}.{debate_context}

Email:
From: {email['from']}
Subject: {email['subject']}
Body: {email['body']}

Return ONLY valid JSON:
{{
  "stance": "Your 2-3 sentence take on this email and how to handle it, in your personality",
  "key_argument": "One punchy sentence — your strongest argument for your approach",
  "vote": "aggressive|diplomatic|analytical",
  "draft_reply": "Your version of a reply to this email, written in your personality (3-5 sentences)"
}}"""
    resp = client.chat.completions.create(
        model=GROQ_MODEL,
        messages=[
            {"role": "system", "content": personas[agent_id]},
            {"role": "user",   "content": prompt},
        ],
        temperature=0.7, max_tokens=600,
    )
    raw = resp.choices[0].message.content.strip().replace("```json","").replace("```","").strip()
    return json.loads(raw)


def call_consensus(client, email, rex_data, sage_data, nova_data):
    prompt = f"""Three AI agents debated how to reply to this email:

Email: From {email['from']}: {email['subject']}
Body: {email['body']}

Agent Rex (aggressive) said: {rex_data['stance']}
Rex's draft: {rex_data['draft_reply']}

Agent Sage (diplomatic) said: {sage_data['stance']}
Sage's draft: {sage_data['draft_reply']}

Agent Nova (analytical) said: {nova_data['stance']}
Nova's draft: {nova_data['draft_reply']}

Synthesize the best elements from all three into one final reply. Take Rex's urgency, Sage's empathy, and Nova's structure.

Return ONLY valid JSON:
{{
  "category": "urgent|action_required|informational|low_priority|spam",
  "priority": "1 - critical|2 - high|3 - medium|4 - low",
  "verdict": "One sentence explaining which agent won the debate and why",
  "consensus_reply": "The final synthesized reply — professional, effective, 4-6 sentences"
}}"""
    resp = client.chat.completions.create(
        model=GROQ_MODEL,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.4, max_tokens=700,
    )
    raw = resp.choices[0].message.content.strip().replace("```json","").replace("```","").strip()
    return json.loads(raw)


def run_war_room(email):
    client = Groq(api_key=GROQ_API_KEY)
    results = {}

    # Round 1 — each agent states position
    for agent_id in ["rex", "sage", "nova"]:
        results[agent_id] = call_agent(client, agent_id, email)

    # Round 2 — rebuttals
    debate_log = []
    for agent_id in ["rex", "sage", "nova"]:
        others = "\n".join([
            f"Agent {aid.upper()}: {results[aid]['key_argument']}"
            for aid in ["rex", "sage", "nova"] if aid != agent_id
        ])
        rebuttal = call_agent(client, agent_id, email, context=others)
        results[f"{agent_id}_rebuttal"] = rebuttal
        debate_log.append({"agent": agent_id, "text": rebuttal["key_argument"]})

    # Consensus
    consensus = call_consensus(client, email, results["rex"], results["sage"], results["nova"])
    results["consensus"] = consensus

    st.session_state.memory.append({
        "ts":       datetime.now().strftime("%H:%M:%S"),
        "subject":  email["subject"][:22],
        "decision": consensus["category"],
        "winner":   consensus["verdict"][:40],
    })
    return results, debate_log


# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div class="sb-header">
        <div class="sb-logo">⚔ War Room</div>
        <div class="sb-tagline">3 agents · 1 inbox · Groq AI</div>
    </div>
    """, unsafe_allow_html=True)

    debates = st.session_state.debates
    n_u = sum(1 for d in debates.values() if d.get("consensus",{}).get("category") == "urgent")
    n_a = sum(1 for d in debates.values() if d.get("consensus",{}).get("category") == "action_required")
    n_i = sum(1 for d in debates.values() if d.get("consensus",{}).get("category") == "informational")

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

    st.markdown('<div class="sb-section-title" style="padding:14px 20px 0;">Inbox</div>', unsafe_allow_html=True)

    sorted_emails = sorted(
        st.session_state.emails,
        key=lambda e: {"urgent":0,"action_required":1,"informational":2,"low_priority":3,"spam":4}
                      .get(debates.get(e["id"],{}).get("consensus",{}).get("category",""), 5)
    )

    for em in sorted_emails:
        d = debates.get(em["id"])
        if d:
            cat = d.get("consensus",{}).get("category","low_priority")
            icon, label, badge_cls = CATEGORY_CONFIG.get(cat, ("⚪","Low","badge-low"))
            badge = f'<span class="badge {badge_cls}">{icon} {label}</span>'
        else:
            badge = f'<span class="badge badge-new">{"● New" if not em["read"] else "—"}</span>'

        is_active = em["id"] == st.session_state.selected_id
        st.markdown(f"""
        <div class="email-item {'active' if is_active else ''}">
            <div class="ei-top">
                <span class="ei-name {'unread' if not em['read'] else ''}">{em['from_name']}</span>
                <span class="ei-time">{em['time']}</span>
            </div>
            <div class="ei-subject {'unread' if not em['read'] else ''}">{em['subject']}</div>
            <div>{badge}</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Open", key=f"btn_{em['id']}", use_container_width=True):
            st.session_state.selected_id = em["id"]
            em["read"] = True
            st.rerun()

    st.markdown('<div style="padding:12px 20px;">', unsafe_allow_html=True)
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

    if st.session_state.memory:
        st.markdown('<div class="sb-section">', unsafe_allow_html=True)
        st.markdown('<div class="sb-section-title">Agent Memory</div>', unsafe_allow_html=True)
        for m in reversed(st.session_state.memory[-4:]):
            st.markdown(f'<div class="memory-item"><span>{m["ts"]}</span> {m["subject"]}… → {m["decision"]}</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)


# ── Main ──────────────────────────────────────────────────────────────────────
if not st.session_state.selected_id:
    st.markdown("""
    <div class="empty-state">
        <div class="empty-icon">⚔</div>
        <div class="empty-title">The War Room awaits</div>
        <div class="empty-sub">Select an email and watch Rex, Sage, and Nova debate the best response in real time.</div>
    </div>
    """, unsafe_allow_html=True)

else:
    email = next((e for e in st.session_state.emails if e["id"] == st.session_state.selected_id), None)
    if email:
        debate = debates.get(email["id"])

        badge_html = ""
        if debate:
            cat = debate.get("consensus",{}).get("category","low_priority")
            icon, label, badge_cls = CATEGORY_CONFIG.get(cat, ("⚪","Low","badge-low"))
            badge_html = f'<span class="badge {badge_cls}" style="font-size:10px;">{icon} {label}</span>'

        st.markdown(f"""
        <div class="email-header">
            <div class="email-title">{email['subject']}</div>
            <div class="email-meta">
                <span>From: <span>{email['from']}</span></span>
                <span>·</span><span>{email['time']}</span>
                {badge_html}
            </div>
        </div>
        """, unsafe_allow_html=True)

        _, col_btn = st.columns([3, 1])
        with col_btn:
            btn_label = "↺ New Debate" if debate else "⚔ Start War Room"
            if st.button(btn_label, key="war_btn"):
                with st.spinner("Agents assembling..."):
                    try:
                        result, log = run_war_room(email)
                        result["debate_log"] = log
                        st.session_state.debates[email["id"]] = result
                        reply_key = f"reply_{email['id']}"
                        if reply_key in st.session_state:
                            del st.session_state[reply_key]
                        st.rerun()
                    except Exception as ex:
                        st.error(f"Error: {ex}")

        st.markdown(f"""
        <div class="email-body-section">
            <div class="section-eyebrow">Message</div>
            <div class="email-body-text">{email['body']}</div>
        </div>
        """, unsafe_allow_html=True)

        if debate:
            rex  = debate.get("rex", {})
            sage = debate.get("sage", {})
            nova = debate.get("nova", {})
            rex_r  = debate.get("rex_rebuttal", rex)
            sage_r = debate.get("sage_rebuttal", sage)
            nova_r = debate.get("nova_rebuttal", nova)

            st.markdown(f"""
            <div class="warroom-section">
                <div class="warroom-title">⚔ The War Room</div>
                <div class="warroom-sub">Three agents read the email, stated positions, then debated each other.</div>
                <div class="agents-grid">
                    <div class="agent-card agent-rex">
                        <div class="agent-header">
                            <div class="agent-avatar avatar-rex">🔴</div>
                            <div>
                                <div class="agent-name rex">Agent Rex</div>
                                <div class="agent-role">Aggressive · Direct</div>
                            </div>
                        </div>
                        <div class="agent-stance">{rex.get('stance','...')}</div>
                        <div class="agent-vote">
                            <div class="vote-label">Key argument</div>
                            <div class="vote-text vote-rex">"{rex_r.get('key_argument', rex.get('key_argument',''))}"</div>
                        </div>
                    </div>
                    <div class="agent-card agent-sage">
                        <div class="agent-header">
                            <div class="agent-avatar avatar-sage">🔵</div>
                            <div>
                                <div class="agent-name sage">Agent Sage</div>
                                <div class="agent-role">Diplomatic · Empathetic</div>
                            </div>
                        </div>
                        <div class="agent-stance">{sage.get('stance','...')}</div>
                        <div class="agent-vote">
                            <div class="vote-label">Key argument</div>
                            <div class="vote-text vote-sage">"{sage_r.get('key_argument', sage.get('key_argument',''))}"</div>
                        </div>
                    </div>
                    <div class="agent-card agent-nova">
                        <div class="agent-header">
                            <div class="agent-avatar avatar-nova">🟢</div>
                            <div>
                                <div class="agent-name nova">Agent Nova</div>
                                <div class="agent-role">Analytical · Strategic</div>
                            </div>
                        </div>
                        <div class="agent-stance">{nova.get('stance','...')}</div>
                        <div class="agent-vote">
                            <div class="vote-label">Key argument</div>
                            <div class="vote-text vote-nova">"{nova_r.get('key_argument', nova.get('key_argument',''))}"</div>
                        </div>
                    </div>
                </div>
            """, unsafe_allow_html=True)

            log = debate.get("debate_log", [])
            if log:
                bubbles = ""
                for entry in log:
                    a = AGENTS[entry["agent"]]
                    bubbles += f"""
                    <div class="debate-bubble">
                        <div class="bubble-avatar {a['avatar_cls']}">{a['emoji']}</div>
                        <div class="bubble-content">
                            <div class="bubble-name {a['name_cls']}">Agent {a['name']}</div>
                            <div class="bubble-text">{entry['text']}</div>
                        </div>
                    </div>"""
                st.markdown(f"""
                <div class="debate-section">
                    <div class="debate-title">Rebuttal Round</div>
                    {bubbles}
                </div>
                """, unsafe_allow_html=True)

            consensus = debate.get("consensus", {})
            st.markdown(f"""
                <div class="consensus-card">
                    <div class="consensus-header">
                        <span class="consensus-icon">🤝</span>
                        <span class="consensus-label">Consensus Reached · {consensus.get('priority','—').title()}</span>
                    </div>
                    <div class="consensus-verdict">"{consensus.get('verdict','')}"</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

            st.markdown('<div class="reply-section">', unsafe_allow_html=True)
            st.markdown('<div class="section-eyebrow" style="margin-bottom:10px;">Consensus Reply</div>', unsafe_allow_html=True)

            reply_key = f"reply_{email['id']}"
            if reply_key not in st.session_state:
                st.session_state[reply_key] = consensus.get("consensus_reply", "")

            edited = st.text_area("", value=st.session_state[reply_key],
                                  height=160, key=f"ta_{email['id']}", label_visibility="collapsed")
            st.session_state[reply_key] = edited

            c1, c2, c3 = st.columns([1, 1, 2])
            with c1:
                if st.button("📋 Copy", key=f"copy_{email['id']}"):
                    st.toast("Copied!")
            with c2:
                if st.button("↺ New Debate", key=f"redebate_{email['id']}"):
                    with st.spinner("Agents reconvening..."):
                        try:
                            result, log = run_war_room(email)
                            result["debate_log"] = log
                            st.session_state.debates[email["id"]] = result
                            if reply_key in st.session_state:
                                del st.session_state[reply_key]
                            st.rerun()
                        except Exception as ex:
                            st.error(str(ex))
            st.markdown('</div>', unsafe_allow_html=True)
