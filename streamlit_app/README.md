# ✉ Email Assistant Agent

> An intelligent email agent where three AI agents debate every email — Rex fights, Sage empathizes, Nova analyzes — then reach a consensus reply.

**Live App:** https://email-assistant-agent-8qugdzcujtkrwaezy5vqjf.streamlit.app/

**Demo Video:** https://www.loom.com/share/dbeb176a5dbc4417b6922f65a9735d4b

---

## What is this?

A multi-agent email assistant built for the Intelligent Software Agents course. Three specialized AI agents debate how to respond to every email, then synthesize a consensus reply.

| Agent | Personality | Strategy |
|---|---|---|
| 🔴 Rex | Aggressive · Direct | Immediate escalation, no excuses |
| 🔵 Sage | Diplomatic · Empathetic | Lead with empathy, preserve relationship |
| 🟢 Nova | Analytical · Strategic | Root cause, structured options |
| 🤝 Consensus | Synthesizer | Best of all three |

---

## Agent Loop — Perceive → Decide → Act

```
PERCEIVE  →  Read email (sender, subject, body)
DECIDE    →  5 Groq API calls:
                Rex stance → Sage stance → Nova stance
                Rex rebuttal → Sage rebuttal → Nova rebuttal
                Consensus builder synthesizes all three
ACT       →  Update inbox, show debate, draft reply, log memory
```

---

## Quickstart

```bash
git clone https://github.com/MohorBhattacharya/email-assistant-agent.git
cd email-assistant-agent
pip install -r requirements.txt

# Add your Groq API key in streamlit_app/app.py:
# GROQ_API_KEY = "gsk_..."

streamlit run streamlit_app/app.py
```

Get a free Groq API key at **console.groq.com** — no credit card needed.

---

## Features

- **War Room debate** — 3 agents with distinct personalities argue the best response
- **Rebuttal round** — agents see each other's arguments and push back
- **Consensus verdict** — declares which approach won and why
- **Editable reply** — human reviews and approves before sending
- **Priority inbox** — emails auto-sort by urgency after analysis
- **Agent memory** — sidebar logs all decisions with timestamps
- **Custom emails** — add your own emails to test the agent

---

## Commit Checkpoints

| Commit | Description |
|---|---|
| `init` | Basic Streamlit UI + Groq API integration |
| `feat: JSON schema` | Structured output from LLM |
| `feat: classification` | Urgent / action / info / spam categories |
| `feat: priority sort` | Inbox re-sorts after analysis |
| `feat: memory log` | Agent tracks past decisions |
| `feat: reply regen` | Human-in-the-loop reply editing |
| `feat: war room` | 3 agents debate every email (Rex, Sage, Nova) |
| `fix: rebuttal rendering` | Chat bubbles render correctly |
| `docs: add demo video` | Loom demo link added |

---

## Tech Stack

- **UI:** Streamlit
- **LLM:** Groq — llama-3.3-70b-versatile
- **Deployment:** Streamlit Community Cloud
- **Language:** Python 3.9+

---

## Requirements

```
groq>=0.9.0
streamlit>=1.35.0
```
