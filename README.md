
---

```markdown
# VaakKalp — Voice Legacy
## Preserving Humanity's Endangered Oral Heritage with Multi-Agent AI

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)]()
[![Built with ADK](https://img.shields.io/badge/Built%20with-Google%20ADK-blue)]()
[![Track: Agents for Good](https://img.shields.io/badge/Track-Agents%20for%20Good-green)]()
[![Tests](https://img.shields.io/badge/Tests-22%20passing-brightgreen)]()

> "Every voice carries a universe. VaakKalp ensures no universe goes silent."

---

## The Problem
- **220** languages lost in India in the last 50 years
- **191** endangered languages in India today (UNESCO)
- **1 language dies every 2 weeks** globally — taking millennia of knowledge with it

## The Solution
VaakKalp is a multi-agent AI system built on Google's Agent Development Kit (ADK) that:
1. Conducts intelligent oral history interviews in any language
2. Transcribes and translates endangered dialects in real time
3. Enriches cultural references with contextual annotations
4. Structures raw conversations into organized digital memoirs
5. Alerts researchers when critically endangered languages are documented

## Architecture

[Architecture diagram image here]

### Agents
| Agent | Role | ADK Feature Used |
|-------|------|-----------------|
| Orchestrator | Routes tasks, manages state | Hierarchical composition |
| Interview Conductor | Conducts dynamic interviews | Tool use, Long-term memory |
| Transcription & Translation | Converts voice, detects dialect | MCP tools |
| Cultural Enricher | Annotates cultural references | MCP tools |
| Story Organizer | Structures memoir chapters | Long-context management |
| Archive Publisher | Publishes digital memoir | MCP tools, Cloud Storage |
| Preservation Alert | Alerts researchers | MCP tools, external APIs |

### MCP Servers
| Server | Wraps | Purpose |
|--------|-------|---------|
| UNESCO Language Atlas MCP | UNESCO API | Language criticality scoring |
| Translation MCP | Google Translate + Bhashini | Low-resource language support |
| Cultural Knowledge Graph MCP | Custom knowledge base | Cultural annotation |
| Archive & Alert MCP | Cloud Storage + Notifications | Storage and researcher alerts |

## Course Concepts Demonstrated
- [x] Multi-agent system (ADK) — 7-agent hierarchy
- [x] MCP Servers — 4 custom servers
- [x] Antigravity — live endangered language processing demo
- [x] Security features — consent workflow, guardrails, data sovereignty
- [x] Deployability — Google Cloud Run with full observability
- [x] Agent Skills — Cultural Interviewer + Cultural Archivist skills

## Project Structure
```
vaakkalp/
├── agents/
│   ├── orchestrator.py          # Root orchestrator agent
│   ├── interview_conductor.py   # Interview agent
│   ├── transcription_translation.py
│   ├── cultural_enricher.py
│   ├── story_organizer.py
│   ├── archive_publisher.py
│   └── preservation_alert.py
├── mcp_servers/
│   ├── unesco_language_atlas_mcp.py
│   ├── translation_mcp.py
│   ├── cultural_knowledge_mcp.py
│   └── archive_alert_mcp.py
├── security/
│   ├── consent_manager.py
│   ├── content_guardrails.py
│   ├── input_validator.py
│   └── data_sovereignty.py
├── skills/
│   ├── cultural_interviewer_skill.py
│   └── cultural_archivist_skill.py
├── observability/
│   └── logging.py
├── frontend/
│   └── app.py                   # Web interface (Gradio/Streamlit)
├── tests/
│   ├── test_agents.py
│   ├── test_mcp_servers.py
│   └── test_security.py
├── Dockerfile
├── deploy.sh
├── requirements.txt
├── .env.example                 # NEVER commit .env — contains no real keys
└── README.md
```

## Setup Instructions

### Prerequisites
- Python 3.11+
- Google Cloud account with billing enabled
- Google AI Studio API key
- Google Cloud Translation API supporting all 22 scheduled Indian languages access (free registration at bhashini.gov.in)

### Local Setup
```bash
# Clone the repository
git clone https://github.com/guhask/vaakkalp
cd vaakkalp

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure environment (copy example, fill in your keys)
cp .env.example .env
# Edit .env with your API keys — NEVER commit this file

# Run locally
python -m uvicorn main:app --reload
# Open http://localhost:8000
```

### Cloud Deployment
```bash
# Authenticate with Google Cloud
gcloud auth login
gcloud config set project YOUR_PROJECT_ID

# Deploy (single command)
chmod +x deploy.sh
./deploy.sh

# Your VaakKalp instance will be live at the Cloud Run URL printed on completion
```

## Security Notes
- NEVER include API keys in code or commits
- All user audio is encrypted at rest in Cloud Storage
- Community consent is logged before any processing begins
- Sacred content is automatically routed to restricted-access archives

## Contributing
This project was built as a Kaggle Capstone submission. Contributions welcome post-competition.

## License
MIT License — with the additional requirement that any derivative work must maintain
community data sovereignty controls and cannot be used for commercial exploitation of
indigenous cultural content without explicit community consent.
```

---
