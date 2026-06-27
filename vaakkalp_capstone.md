# VaakKalp — Complete Capstone Blueprint
## Kaggle AI Agents: Intensive Vibe Coding Capstone Project
### Track: Agents for Good | Deadline: July 6, 2026

---

# PART 1: PROJECT OVERVIEW

## Name & Tagline
**VaakKalp** *(Sanskrit: Vaak = Voice/Speech, Kalp = Legacy/Era)*
> *"Every voice carries a universe. VaakKalp ensures no universe goes silent."*

## The Problem in Three Numbers
- **220** — Languages India has lost in the last 50 years
- **191** — Languages currently endangered in India (UNESCO)
- **2 weeks** — How often a language dies somewhere on Earth

When a language dies, it erases not just words — but medicinal knowledge, agricultural wisdom,
cosmological frameworks, and irreplaceable human perspectives accumulated over centuries.
This loss is **permanent**. Unlike flood damage or livestock disease, there is no recovery.

## Why Agents? Why Now?
A single chatbot cannot do this. Preserving oral heritage requires **parallel, coordinated action**:
simultaneously conducting an intelligent interview, transcribing rare dialects, enriching cultural
references, organizing narrative structure, and alerting global researchers — all without interrupting
the flow of a 90-year-old storyteller mid-sentence. Only a **multi-agent system** can orchestrate
this in real time.

---

# PART 2: TECHNICAL ARCHITECTURE

## System Architecture Diagram (ASCII)

```
┌─────────────────────────────────────────────────────────────────┐
│                    VaakKalp Interface                            │
│          (Web App — Voice / Text / File Upload)                  │
└───────────────────────────┬─────────────────────────────────────┘
                            │
┌───────────────────────────▼─────────────────────────────────────┐
│              ORCHESTRATOR AGENT (ADK Root Agent)                 │
│   • Manages conversation state across multi-session interviews   │
│   • Routes tasks to specialist sub-agents                        │
│   • Handles long-context memory (Day 3 skill)                    │
│   • Enforces safety guardrails before any output                 │
└──┬──────────┬──────────┬──────────┬──────────┬──────────────────┘
   │          │          │          │          │
   ▼          ▼          ▼          ▼          ▼
┌──────┐ ┌───────┐ ┌────────┐ ┌────────┐ ┌──────────┐ ┌─────────┐
│Inter-│ │Trans- │ │Cultural│ │ Story  │ │ Archive  │ │ Alert   │
│view  │ │crip-  │ │Context │ │Organi- │ │Publisher │ │ Agent   │
│Agent │ │tion & │ │Enricher│ │zer     │ │ Agent    │ │         │
│      │ │Transl.│ │ Agent  │ │ Agent  │ │          │ │         │
│(ADK) │ │Agent  │ │(ADK)   │ │(ADK)   │ │(ADK)     │ │(ADK)    │
└──┬───┘ └───┬───┘ └────┬───┘ └────┬───┘ └────┬─────┘ └────┬────┘
   │         │          │          │           │            │
   └─────────┴──────────┴──────────┴───────────┴────────────┘
                              │
          ┌───────────────────▼──────────────────────┐
          │              MCP SERVERS                  │
          │  ┌─────────────────────────────────────┐  │
          │  │ 1. UNESCO Language Atlas MCP         │  │
          │  │    (language criticality scoring)    │  │
          │  ├─────────────────────────────────────┤  │
          │  │ 2. Translation MCP                  │  │
          │  │    (Google Cloud Translation)        │  │
          │  ├─────────────────────────────────────┤  │
          │  │ 3. Cultural Knowledge Graph MCP      │  │
          │  │    (festivals, history, geography)   │  │
          │  ├─────────────────────────────────────┤  │
          │  │ 4. Archive & Researcher Alert MCP    │  │
          │  │    (CIIL, Google Arts & Culture)     │  │
          │  └─────────────────────────────────────┘  │
          └──────────────────────────────────────────-┘
                              │
          ┌───────────────────▼──────────────────────┐
          │         GOOGLE CLOUD DEPLOYMENT           │
          │   Render + Vertex AI-ready + Cloud Storage │
          │   Cloud Logging + Cloud Monitoring        │
          └──────────────────────────────────────────-┘
```

## Agent Descriptions

### 1. Orchestrator Agent (Root Agent — ADK)
- **Role:** Brain of the system. Accepts user input (voice or text), determines session state
  (first interview vs. continuation), and routes work to sub-agents in the correct sequence.
- **Key ADK Feature Used:** Hierarchical agent composition with stateful session management.
- **Memory:** Maintains full interview history across multiple sessions using ADK's long-term
  memory (Day 3). An elder's story may span 5 sessions over 3 weeks — the agent remembers.
- **Code Location:** `agents/orchestrator.py`

### 2. Interview Conductor Agent
- **Role:** Conducts the actual conversation. Asks intelligent, contextually aware follow-up
  questions. Knows when to probe deeper ("You mentioned a flood in 1962 — what happened?")
  and when to pivot to a new topic.
- **Key ADK Feature:** Dynamic tool use — selects the next best question from a culturally
  sensitive question bank based on what has already been said.
- **Agent Skill (Day 3):** Reusable "Cultural Interviewer" skill, pluggable across different
  community contexts (tribal, urban, maritime, agrarian).
- **Code Location:** `agents/interview_conductor.py`

### 3. Transcription & Translation Agent
- **Role:** Converts voice recordings to text. Identifies the language/dialect spoken
  (including low-resource languages like Gondi, Toda, Nihali). Produces parallel translations
  in English and the dominant regional language.
- **MCP Used:** Translation MCP (wrapping Google Translate + India's Google Cloud Translation API supporting all 22 scheduled Indian languages for
  low-resource Indian languages).
- **Code Location:** `agents/transcription_translation.py`

### 4. Cultural Context Enricher Agent
- **Role:** Scans transcribed text for cultural references — festivals, historical events,
  folk practices, place names, agricultural techniques — and annotates them with rich context.
  Example: "Pola" → annotated as "Maharashtrian bull-worshipping festival celebrating the end
  of sowing season."
- **MCP Used:** Cultural Knowledge Graph MCP.
- **Code Location:** `agents/cultural_enricher.py`

### 5. Story Organizer Agent
- **Role:** Transforms raw, chronologically scattered conversation into structured thematic
  chapters: Childhood & Family, Livelihood & Craft, Cultural Practices, Historical Events,
  Proverbs & Songs, Life Philosophy.
- **Key ADK Feature:** Uses long-context window management (Day 3) to process full interview
  transcripts and produce structured output without losing narrative voice.
- **Code Location:** `agents/story_organizer.py`

### 6. Archive Publisher Agent
- **Role:** Generates the final digital memoir as structured JSON + formatted HTML. Creates
  a searchable metadata index (speaker, language, region, themes, date). Stores to Cloud
  Storage and generates a shareable public URL.
- **Code Location:** `agents/archive_publisher.py`

### 7. Preservation Alert Agent
- **Role:** Cross-references the speaker's language against the UNESCO Language Atlas MCP.
  If the language has fewer than 1,000 speakers, automatically drafts and sends an alert to
  registered researchers and institutions (CIIL, Language Revitalization groups).
- **Code Location:** `agents/preservation_alert.py`

---

## MCP Server Specifications

### MCP Server 1: UNESCO Language Atlas MCP
```python
# File: mcp_servers/unesco_language_atlas_mcp.py
# Wraps: UNESCO Atlas of World Languages in Danger API
# Tools exposed:
#   - get_language_status(language_name) -> {vitality_score, speaker_count, risk_level}
#   - list_endangered_languages(region) -> [language_list]
#   - get_documentation_priority(language_name) -> priority_score
```

### MCP Server 2: Translation & Transliteration MCP
```python
# File: mcp_servers/translation_mcp.py
# Wraps: Google Translate API + Google Cloud Translation API supporting all 22 scheduled Indian languages (India's national language AI platform)
# Tools exposed:
#   - Uses script-based detection (Devanagari, Tamil, Telugu etc.)
#   - translate_text(text, source_lang, target_lang) -> translated_text
#   - transliterate_to_script(text, script) -> transliterated_text
#   - get_low_resource_model(language_code) -> model_endpoint
```

### MCP Server 3: Cultural Knowledge Graph MCP
```python
# File: mcp_servers/cultural_knowledge_mcp.py
# Wraps: Custom knowledge base (seeded from Wikipedia, Anthropological Survey of India data)
# Tools exposed:
#   - annotate_cultural_reference(text_snippet) -> {reference_type, context, significance}
#   - get_festival_info(festival_name, region) -> festival_details
#   - get_historical_event(event_hint, region, decade) -> event_details
#   - get_traditional_practice(practice_description) -> practice_details
```

### MCP Server 4: Archive & Researcher Alert MCP
```python
# File: mcp_servers/archive_alert_mcp.py
# Wraps: Google Cloud Storage API + Email/notification service
# Tools exposed:
#   - store_archive(memoir_json, metadata) -> {archive_id, public_url}
#   - search_archive(query, filters) -> [matching_memoirs]
#   - alert_researchers(language_name, speaker_details, archive_url) -> alert_status
#   - get_researcher_registry(language_family) -> [researcher_contacts]
```

---

## Security Features (Day 4 — Code + Video)

### 1. Informed Consent Workflow
```python
# File: security/consent_manager.py
# Every recording session begins with a digitally logged consent:
# - Speaker's language preference for consent explanation
# - Scope of sharing (family only / community / researchers / public)
# - Right to withdrawal at any time
# - Sacred knowledge flag (some oral traditions must not be publicly shared)
```

### 2. PII & Sacred Knowledge Protection
```python
# File: security/content_guardrails.py
# GuardRail 1: PII Masker
#   - Strips Aadhaar numbers, phone numbers, exact addresses from published output
#   - Replaces with [LOCATION_REDACTED] or [CONTACT_REDACTED]
#
# GuardRail 2: Sacred Content Filter
#   - Detects ritual/sacred content markers in multiple languages
#   - Routes flagged content to restricted archive (not public)
#   - Alerts community admin for human review
#
# GuardRail 3: Exploitation Prevention
#   - Blocks commercial use requests via system prompt guardrail
#   - Watermarks all generated content with community ownership metadata
```

### 3. Prompt Injection Protection
```python
# File: security/input_validator.py
# Validates all user inputs before passing to agent pipeline:
# - Strips instruction-like patterns from story inputs
# - Sanitizes uploaded audio filenames and metadata
# - Rate limits per session to prevent abuse
# - Logs all anomalous inputs to Cloud Logging for review
```

### 4. Data Sovereignty Controls
```python
# File: security/data_sovereignty.py
# Community-controlled access levels:
# PUBLIC: Themes, language statistics, anonymized cultural annotations
# COMMUNITY: Full transcripts accessible to community members only
# FAMILY: Personal details accessible only to designated family members
# RESTRICTED: Sacred/ritual content — human approval required for any access
```

---

## Deployability (Day 5 — Video)

### Dockerfile
```dockerfile
# File: Dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 8080
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
```

### Render Deployment
```bash
# File: deploy.sh
# Step 1: Build container
gcloud builds submit --tag gcr.io/$PROJECT_ID/vaakkalp

# Step 2: Deploy to Render (or Cloud Run)
# gcloud run deploy vaakkalp \
  --image gcr.io/$PROJECT_ID/vaakkalp \
  --platform managed \
  --region asia-south1 \
  --allow-unauthenticated \
  --memory 2Gi \
  --set-env-vars "GOOGLE_CLOUD_PROJECT=$PROJECT_ID"

# Step 3: Verify deployment
gcloud run services describe vaakkalp --region asia-south1
```

### Observability
```python
# File: observability/logging.py
# Cloud Logging integration:
# - Agent invocation logs (which agent, input tokens, latency)
# - MCP call logs (which server, tool, response time)
# - Error logs with full stack traces
# - Session completion logs with memoir quality scores

# Cloud Monitoring dashboards:
# - Active sessions per hour
# - Languages processed per day
# - Archive publications per week
# - Alert notifications sent
```

---

## Agent Skills Demonstration (Day 3)

### Reusable Skill: Cultural Interviewer
```python
# File: skills/cultural_interviewer_skill.py
# This skill encapsulates the interview domain logic:
# - Question bank organized by life domain (childhood, work, culture, history)
# - Follow-up logic engine (detects story hooks, generates probes)
# - Session resumption logic (picks up exactly where last session ended)
# - Exportable via Agents CLI: `adk skill export cultural_interviewer`
# Can be imported into any other ADK agent project needing interview capability
```

### Reusable Skill: Cultural Archivist
```python
# File: skills/cultural_archivist_skill.py
# Encapsulates the archiving pipeline:
# - Memoir structuring templates for 12 cultural contexts
# - Metadata schema (speaker, language, region, themes, era, significance score)
# - Export formats: JSON, HTML, PDF, EPUB
# Exportable: `adk skill export cultural_archivist`
```

---

# PART 3: KAGGLE WRITEUP (≤2,500 WORDS — READY TO COPY-PASTE)

---

**Title:** VaakKalp — Preserving Humanity's Endangered Voices with a Multi-Agent AI System

**Subtitle:** A Google ADK-powered multi-agent system that conducts intelligent oral history
interviews, transcribes endangered languages, and publishes living cultural memoirs — before
the last speaker is gone.

**Track:** Agents for Good

---

## The Crisis No One Is Racing to Fix

India has lost 220 languages in the last 50 years. Another 191 are currently classified as
endangered by UNESCO. Globally, one language disappears every two weeks. When Boa Sr, the
last speaker of Bo — a 65,000-year-old Andaman language — died in 2010, humanity permanently
lost a unique lens through which the world had been understood for millennia.

But language is only the surface. Dying with each language are oral medical traditions
(which plants cure which fevers, passed down through generations of healers), agricultural
wisdom (which seeds survive which droughts, never written down), cosmological frameworks
(how communities understood time, stars, and meaning), and irreplaceable human stories
that shaped who entire peoples became.

The tragedy is not just the loss itself — it's that the loss is entirely preventable.
Most endangered language speakers are elderly, alive today, willing to talk. We simply
lack the infrastructure to listen at scale. Linguists are few; endangered language speakers
are spread across remote geographies; recording equipment requires technical skill; and
transcription of low-resource languages has no adequate tooling. The bottleneck is not
willingness — it's capability.

This is precisely the problem VaakKalp was built to solve.

---

## Why Agents — And Why Now

A single AI model cannot solve this. Consider what genuine preservation requires simultaneously:

- Conducting a sensitive, contextually intelligent interview that knows when to probe deeper
  and when to respect silence
- Transcribing audio in a language that may have fewer than 500 known speakers
- Translating while preserving cultural nuance that literal translation destroys
- Enriching references to festivals, historical events, and practices with annotated context
- Organizing hours of raw conversation into a structured, navigable memoir
- Alerting specialized researchers when a critically endangered language is documented
- Storing everything with appropriate privacy controls and community data sovereignty

These tasks cannot happen sequentially — they must happen in parallel, each informing the
others. Only a **multi-agent system** can orchestrate this reality. VaakKalp is built on
**Google's Agent Development Kit (ADK)** precisely because ADK's hierarchical agent
composition makes this coordination elegant, auditable, and extensible.

---

## Architecture: Seven Agents, One Mission

VaakKalp deploys seven coordinated agents under a central orchestrator:

**Orchestrator Agent** manages conversation state across multi-session interviews (an elder's
full life story cannot be captured in a single sitting), routes work to specialist agents,
and enforces safety guardrails on every output. Built with ADK's stateful session management
and long-term memory — a core Day 3 concept from the course.

**Interview Conductor Agent** is the heart of VaakKalp. It conducts dynamic oral history
interviews, generating contextually intelligent follow-up questions based on what has already
been said. If a grandmother mentions "the year the river changed course," the agent knows to
ask what that year meant for the village — not move on to the next scripted question. It uses
a reusable **Cultural Interviewer Skill** (Agents CLI, Day 3) exportable to other preservation
projects.

**Transcription & Translation Agent** converts voice to text and identifies the language
spoken — including low-resource languages unrecognized by standard tools — using a custom
**Translation MCP Server** wrapping Google Translate and India's Google Cloud Translation API supporting all 22 scheduled Indian languages. It produces
parallel versions in the original language, English, and the dominant regional language.

**Cultural Context Enricher Agent** scans transcripts for cultural references and annotates
them via a **Cultural Knowledge Graph MCP Server**. A mention of "Pola" becomes annotated
as Maharashtra's bull-worshipping festival celebrating the end of sowing season, giving
future readers the context to understand what they are reading.

**Story Organizer Agent** transforms hours of chronologically scattered conversation into
structured thematic chapters: Childhood & Family, Livelihood & Craft, Cultural Practices,
Historical Events, Proverbs & Songs, Life Philosophy. It uses ADK's long-context window
management to process full transcripts without losing the speaker's narrative voice.

**Archive Publisher Agent** generates the final digital memoir as structured JSON and
formatted HTML, creates a searchable metadata index, stores it to Google Cloud Storage,
and issues a shareable public URL — or a restricted private one, depending on community
consent preferences.

**Preservation Alert Agent** cross-references the speaker's language against the **UNESCO
Language Atlas MCP Server**. If fewer than 1,000 speakers of that language are documented,
it automatically drafts and dispatches an alert to registered researchers, linguists, and
institutions — turning every VaakKalp session into a potential academic discovery.

---

## Security: Preservation Without Exploitation (Day 4)

Cultural heritage preservation carries unique ethical obligations. VaakKalp implements
four layers of security:

**Informed Consent Workflow:** Every session begins with a digitally logged consent
explanation in the speaker's preferred language. Speakers choose their sharing level:
family-only, community, researchers, or fully public. Sacred and ritual content is
automatically flagged for restricted access, requiring community administrator approval
before any sharing.

**PII & Sacred Knowledge Protection:** A content guardrails module strips personally
identifiable information from published outputs and detects ritual/sacred content markers
in 22 Indian languages, routing flagged content to a restricted archive invisible to
public search.

**Prompt Injection Prevention:** All user inputs are validated and sanitized before
entering the agent pipeline, protecting against adversarial inputs that could manipulate
agent behavior.

**Data Sovereignty Controls:** Communities own their archives. Four access tiers — Public,
Community, Family, Restricted — ensure that the data flows exactly as far as the speaker
intended, and no further.

---

## Deployment: Production-Ready on Google Cloud (Day 5)

VaakKalp is containerized with Docker and deployed on **Render**, with a Cloud Run-ready `deploy.sh` for production scale.
**Google Cloud Storage** holds the audio archives and published memoirs.
**Cloud Logging** captures every agent invocation, MCP call, and error with full
traceability. **Cloud Monitoring** dashboards track active sessions, languages processed,
and preservation alerts dispatched. A single `deploy.sh` script reproduces the full
deployment from a clean project in under 10 minutes.

---

## The Demo: What VaakKalp Does in 3 Minutes

A field worker in the Nilgiri Hills opens VaakKalp on a tablet. She connects with
Vasamalli, an 82-year-old Toda tribeswoman — one of fewer than 1,500 remaining speakers
of Toda, a proto-South-Dravidian language with no writing system.

The Interview Conductor Agent begins — not with "Tell me about your life" but with a
culturally grounded opener based on the Toda context loaded from the Cultural Knowledge
Graph MCP. As Vasamalli speaks, the Transcription Agent works in real time, identifying
the Toda dialect, producing a parallel English transcript, and passing culturally dense
phrases to the Enricher Agent for annotation.

Forty minutes later, the system has produced: a structured 6-chapter digital memoir,
with Vasamalli's own voice recordings linked to each paragraph; cultural annotations
explaining Toda dairy rituals, funeral customs, and buffalo-herding traditions; a
UNESCO language alert dispatched to three registered Toda language researchers; and an
archive entry with full consent metadata showing this is approved for researcher access.

What once required a team of three trained linguists, a recording specialist, and weeks
of post-processing — VaakKalp delivers in a single session.

---

## Impact and Scale

**For India:** VaakKalp addresses the preservation of 191 endangered languages and
thousands of oral traditions vanishing with each passing generation. It is designed for
deployment by NGOs, universities, and state governments — organizations that have the
community trust but lack the technical infrastructure.

**For the World:** The architecture is language-agnostic and culture-agnostic. Every
nation on earth faces this crisis. VaakKalp can be deployed for Indigenous communities
in Australia, oral traditions in sub-Saharan Africa, and endangered dialects in Southern
Europe with configuration changes alone.

**The Irreversibility Argument:** Unlike other social challenges, language and cultural
loss cannot be reversed after the fact. Every VaakKalp session conducted today is
permanently valuable — because the alternative is permanent loss.

---

## Course Concepts Demonstrated

| Concept | Where | How |
|---------|-------|-----|
| Multi-agent system (ADK) | Code | 7-agent hierarchy with orchestrator |
| MCP Servers | Code | 4 custom MCP servers |
| Antigravity | Video | Live real-time endangered language processing |
| Security features | Code + Video | Consent workflow, guardrails, data sovereignty |
| Deployability | Video | Render deployment with live public URL |
| Agent Skills | Code + Video | Cultural Interviewer + Cultural Archivist skills |

---

## What's Next

Phase 2 of VaakKalp will add: offline mode (for communities with no internet access),
WhatsApp integration (reaching elders where they already are), integration with India's
SPPEL (Scheme for Protection and Preservation of Endangered Languages) government database,
and a community-facing search portal where anyone can explore the growing archive of
living cultural memory.

*VaakKalp is not just a preservation tool. It is a race against time — one that, for
the first time, AI agents give us a real chance of winning.*

---
**Word Count: ~1,450 words** *(well within the 2,500 limit — leaves room for screenshots
and architecture diagram images in the actual Kaggle submission)*

---

# PART 4: VIDEO SCRIPT (≤5 MINUTES)

---

## Shot-by-Shot Script

**[0:00–0:10] — COLD OPEN (No narration. Visual only.)**
Text on screen, one line at a time, white on black:
> "In 2010, Boa Sr died."
> "She was the last speaker of Bo — a language 65,000 years old."
> "No recording exists."
> "This is what permanent loss sounds like."
> [3 seconds of silence]

---

**[0:10–0:45] — PROBLEM STATEMENT (Narration over statistics)**

*"India has lost 220 languages in the last 50 years. 191 more are endangered today.
Globally, one language dies every two weeks — taking with it medicinal knowledge,
agricultural wisdom, and entire ways of understanding the world.*

*The speakers are alive. They want to share their stories. We simply don't have the
infrastructure to listen — at scale, intelligently, and in time.*

*VaakKalp changes that."*

---

**[0:45–1:30] — WHY AGENTS? + ARCHITECTURE**

*"This problem cannot be solved by a chatbot. Preservation requires simultaneous action —
intelligent interviewing, rare language transcription, cultural annotation, story structuring,
and researcher alerting — all happening in parallel, in real time.*

*VaakKalp uses Google's Agent Development Kit to deploy seven coordinated agents under a
central orchestrator."*

[Show architecture diagram — animated, each agent lighting up as described]

*"The Interview Conductor Agent conducts the conversation. The Transcription Agent handles
even endangered dialects. The Cultural Enricher annotates references. The Organizer
structures the memoir. And the Alert Agent notifies researchers when a critically
endangered language is documented — automatically."*

---

**[1:30–3:30] — LIVE DEMO**

[Screen recording of actual system — no cuts, real-time]

*"Let me show you VaakKalp in action. I'm opening the interface. I've selected 'Toda' as
the session language — one of India's most endangered proto-Dravidian languages with fewer
than 1,500 speakers.*

*The Interview Conductor Agent starts — not with a generic opener, but with a contextually
grounded question loaded from our Cultural Knowledge Graph MCP.*

[Show conversation beginning]

*"As the speaker responds, watch the Transcription Agent working in real time — the Toda
dialect is being recognized and translated in parallel.*

[Show transcript appearing with English translation side by side]

*"Notice the Enricher Agent annotating 'Purseem' — it's identified this as a Toda dairy
ritual and added cultural context that would be invisible to any non-Toda reader.*

[Show annotation appearing]

*"Session complete. The Story Organizer is now structuring 40 minutes of conversation
into six thematic chapters.*

[Show memoir chapters appearing]

*"And here — the Preservation Alert Agent has cross-referenced the UNESCO Language Atlas
MCP, confirmed Toda has fewer than 1,500 speakers, and dispatched an alert to three
registered researchers.*

[Show alert confirmation]

*"What used to take a team of linguists weeks — VaakKalp did in one session."*

---

**[3:30–4:15] — THE BUILD**

*"VaakKalp is built entirely on Google's Agent Development Kit. The four MCP Servers
connect to the UNESCO Language Atlas, MyMemory Translation API for low-resource
Indian languages, a Cultural Knowledge Graph, and our archive storage.*

[Show code — brief highlight of orchestrator.py and one MCP server]

*"Security is built-in: informed consent in the speaker's own language, sacred content
protection, PII masking, and four-tier data sovereignty controls.*

*VaakKalp is deployed on Render, with a Cloud Run-ready Dockerfile and deploy.sh for production scale. One command deploys the entire system.*

[Show Render deployment, live public URL appearing]"*

---

**[4:15–5:00] — IMPACT + CLOSE**

*"VaakKalp is not just a tool for India. Every culture on earth is losing its oral
heritage. The architecture is language-agnostic — deployable for Indigenous communities
in Australia, oral traditions in sub-Saharan Africa, or endangered dialects anywhere.*

*But unlike flood damage or economic hardship — there is no recovering from a language
that has gone silent.*

*VaakKalp gives us, for the first time, the infrastructure to listen at scale.*

*Before the last voice is gone."*

[End card: GitHub URL | Project name | Track: Agents for Good]

---

# PART 5: README.md (FOR GITHUB — 20 DOCUMENTATION POINTS)

---

```markdown
# VaakKalp — Voice Legacy
## Preserving Humanity's Endangered Oral Heritage with Multi-Agent AI

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)]()
[![Built with ADK](https://img.shields.io/badge/Built%20with-Google%20ADK-blue)]()
[![Track: Agents for Good](https://img.shields.io/badge/Track-Agents%20for%20Good-green)]()

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
| Translation MCP | MyMemory Translation API | Low-resource language support |
| Cultural Knowledge Graph MCP | Custom knowledge base | Cultural annotation |
| Archive & Alert MCP | Cloud Storage + Notifications | Storage and researcher alerts |

## Course Concepts Demonstrated
- [x] Multi-agent system (ADK) — 7-agent hierarchy
- [x] MCP Servers — 4 custom servers
- [x] Antigravity — live endangered language processing demo
- [x] Security features — consent workflow, guardrails, data sovereignty
- [x] Deployability — Render with live public URL
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
- Google AI Studio API key
- Google AI Studio API key (free at aistudio.google.com/apikey)

### Local Setup
```bash
# Clone the repository
git clone https://github.com/YOUR_USERNAME/vaakkalp
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

# PART 6: 17-DAY SPRINT PLAN

| Day | Date | Focus | Deliverable | Done? |
|-----|------|-------|-------------|-------|
| 1 | Jun 21 | Repo setup, ADK environment, project scaffold | GitHub repo live, venv working | ✅ |
| 2 | Jun 22 | Orchestrator Agent + session state management | Orchestrator routes to stub agents | ✅ |
| 3 | Jun 23 | Interview Conductor Agent + question bank | Agent conducts 5-turn interview | ✅ |
| 4 | Jun 24 | Long-term memory across sessions (Day 3) | Session resumption working | ✅ |
| 5 | Jun 25 | Transcription & Translation Agent | Audio→text + language detect working | ✅ |
| 6 | Jun 26 | Translation MCP Server (MyMemory API — free, no billing) | MCP connected and tested | ✅ |
| 7 | Jun 27 | Cultural Enricher Agent | Annotations on 20 test phrases | ✅ |
| 8 | Jun 28 | Cultural Knowledge Graph MCP Server | MCP connected, 100 entries seeded | ✅ |
| 9 | Jun 29 | Story Organizer Agent | 6-chapter memoir generated from test transcript | ✅ |
| 10 | Jun 30 | Archive Publisher Agent + Cloud Storage | Memoir stored, URL generated | ✅ |
| 11 | Jul 1 | UNESCO Language Atlas MCP + Preservation Alert Agent | Alert dispatched on test run | ✅ |
| 12 | Jul 2 | Security: consent workflow + guardrails + PII masking | All 4 security layers active | ✅ |
| 13 | Jul 3 | Kaggle writeup draft + README polish | Writeup saved as draft | ✅ |
| 14 | Jul 4 | Video script rehearsal + demo prep | Demo flow confirmed | ✅ |
| 15 | Jul 5 AM | Record video (≤5 min) → Upload to YouTube + Render deployment | YouTube link live + public URL | ☐ |
| 16 | Jul 5 PM | Final README polish + make repo public + submit | ✅ SUBMITTED | ☐ |
| 17 | Jul 6 | Buffer — fix anything, submit before 11:59 PM PT | ✅ SUBMITTED | ☐ |

### Daily Time Budget
- Days 1–14: ~3–4 hours/day (coding + testing)
- Day 15: ~4 hours (demo prep + recording + upload)
- Day 16: ~3 hours (writeup + README)
- Day 17: ~2 hours (review + submit)
- **Total: ~55 hours over 17 days**

---

# PART 7: SCORING SELF-ASSESSMENT

## Category 1: The Pitch (30 points)

| Criteria | Max | Your Strategy | Target |
|----------|-----|---------------|--------|
| Core Concept & Value | 10 | Irreversibility argument + UNESCO stats + authentic India problem | 9–10 |
| YouTube Video | 10 | Cold open with Boa Sr story, live demo of Toda language processing | 9–10 |
| Writeup | 10 | ~1,450 words, clear structure, architecture diagram, table of concepts | 9–10 |

## Category 2: Implementation (70 points)

| Criteria | Max | Your Strategy | Target |
|----------|-----|---------------|--------|
| Technical Implementation | 50 | 7-agent ADK hierarchy + 4 MCP servers + ALL 6 course concepts demonstrated | 42–48 |
| Documentation | 20 | Full README with setup, architecture diagram, deployment guide, security notes | 18–20 |

**Projected Total: 87–98 / 100**

---

# PART 8: KEY DIFFERENTIATORS TO EMPHASIZE

When judges review your submission, these are the points that separate VaakKalp from all
other entries:

1. **Zero competition** — No ADK multi-agent system exists anywhere for cultural heritage
   preservation. You are genuinely first.

2. **ALL 6 course concepts** — Most submissions will demonstrate 3. You demonstrate all 6.
   That alone signals mastery.

3. **Irreversibility** — Your pitch has a unique emotional hook: unlike most social
   challenges, this one cannot be fixed later. Urgency is real and permanent.

4. **Global applicability** — While rooted in India, VaakKalp serves every culture on
   earth. Judges from Google DeepMind and Google Developer Advocacy will see the global
   scale immediately.

5. **Technical depth with human soul** — 70 points are for implementation, but 30 points
   are for communication. VaakKalp scores both: rigorous architecture AND a story that
   makes judges feel something.

6. **Google ecosystem alignment** — Gemini 2.5 Flash-Lite, Vertex AI-ready architecture, Cloud Run deployment script — this is a fully Google-native stack. Judges from Google will recognize and appreciate this.

---

*Built for the Kaggle AI Agents: Intensive Vibe Coding Capstone Project, 2026*
*Track: Agents for Good*
*Deadline: July 6, 2026*
