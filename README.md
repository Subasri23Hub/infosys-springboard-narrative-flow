# Narrative Flow — Story Co-Writer

> *Collaborative AI-powered fiction writing platform built for the Infosys Springboard Programme.*

<br>

![Python](https://img.shields.io/badge/Python-3.10%2B-111008?style=flat-square&logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-1.x-FF4B4B?style=flat-square&logo=streamlit&logoColor=white)
![Ollama](https://img.shields.io/badge/Ollama-Local%20LLM-black?style=flat-square)
![Infosys](https://img.shields.io/badge/Infosys-Springboard-0057A8?style=flat-square)
![Status](https://img.shields.io/badge/Status-Completed-27AE60?style=flat-square)

<br>

---

## About the Project

**Narrative Flow — Story Co-Writer** is an AI-powered web application that enables writers to collaboratively craft fiction with a locally running large language model. Built entirely in Python using Streamlit and Ollama — all story content stays on the user's machine with no cloud dependency, no API keys, and no cost.

This repository is the team submission for the **Infosys Springboard** programme. Each team member has independently developed their own implementation of the Narrative Flow platform.

<br>

---
## Collaborators
- Bhargavi Anakapalli - https://github.com/BhargaviAnakapalli
- Dharmeswaran - https://github.com/dharmes18
- Nithya S - https://github.com/Nithya2405
- Ramya Jayaram - https://github.com/ramyajayaram2006
- SriHarini - https://github.com/Sriharini5
- Dharmeswaran - https://github.com/dharmes18

<br>

---
## The Team

| Member | Folder | Role |
|--------|--------|------|
| **Subasri B** | `Subasri B/` | **Team Lead** — Architecture, UI/UX, LLM Integration, PDF Export, Guardrails, Documentation |
| Bhargavi Anakapalli | `Bhargavi Anakapalli/` | Story co-writer implementation |
| Dharmeswaran | `Dharmeswaran/` | Story co-writer implementation |
| Nithya S | `Nithya S/` | Story co-writer implementation |
| Ramya Jayaram | `Ramya Jayaram/` | Story co-writer implementation |
| Sriharini | `Sriharini/` | Story co-writer implementation |

> **Note:** The full project architecture, documentation, and phase-wise technical reports were designed and authored by the team lead. See `Subasri B/docs/` for complete documentation covering all three phases.

<br>

---

## Repository Structure

```
infosys-springboard-narrative-flow/
│
├── Subasri B/               ← Team Lead 
│   ├── app.py
│   ├── ui_components.py
│   ├── story_engine.py
│   ├── auth.py
│   └── docs/
│       ├── Phase1_Streamlit & UI.docx
│       ├── Phase2_Olama Integration.docx
│       └── Phase3_The Guradrails.docx
│
├── Bhargavi Anakapalli/
├── Dharmeswaran/
├── Nithya S/
├── Ramya Jayaram/
├── Sriharini/
│
└── README.md
```

<br>

---

## Core Technology

| Technology | Role |
|-----------|------|
| **Python** | Primary programming language |
| **Streamlit** | Web application framework — UI, state management, reactive rendering |
| **Ollama** | Local LLM runtime — runs large language models on the user's own hardware |
| **llama3 / qwen2.5** | Default AI models for story generation |
| **ReportLab** | PDF generation and export |

<br>

---

## What the Application Does

Narrative Flow — Story Co-Writer allows users to:

- **Generate fiction** collaboratively with a local AI model across multiple genres and tones
- **Guide the narrative** using writing actions such as Continue, Plot Twist, Dialogue, Flashback, and more
- **Build and view** their manuscript in a formatted book viewer
- **Export** their story as a print-ready PDF or plain text file
- **Develop characters and worlds** using dedicated AI writing tools
- **Manage story history** with per-user accounts and persistent session saving

<br>

---

## How to Run

### Prerequisites
- Python 3.10+
- [Ollama](https://ollama.com) installed

```bash
# Pull the AI model
ollama pull llama3

# Start Ollama
ollama serve
```

### Install & Run
```bash
# Install dependencies
pip install streamlit requests reportlab

# Navigate to any team member's folder and run
streamlit run app.py
```

Open `http://localhost:8501` in your browser.

<br>

---

## Project Phases

| Phase | Description | Status |
|-------|-------------|--------|
| **Phase 1** | UI Design & Streamlit Implementation | ✅ Complete |
| **Phase 2** | Ollama LLM Integration & Prompt Engineering | ✅ Complete |
| **Phase 3** | Guardrails & Content Safety | ✅ Complete |

<br>

---

## Documentation

Full phase-wise technical documentation authored by the team lead is available in `Subasri B/docs/`:

| Document | Description |
|----------|-------------|
| `Phase1_Streamlit & UI.docx` | Phase 1 — UI & Streamlit implementation |
| `Phase2_Olama Integration.docx` | Phase 2 — Ollama integration & prompt engineering |
| `Phase3_The Guardrails.docx` | Phase 3 - The guardrail implementation |

<br>

---

## Programme Details

| | |
|-|-|
| **Programme** | Infosys Springboard |
| **Project** | Narrative Flow — Story Co-Writer |
| **Domain** | Generative AI · Natural Language Processing · Web Development |
| **Tech Track** | Python · Streamlit · Local LLM (Ollama) |

<br>

---

*Narrative Flow — Story Co-Writer · Infosys Springboard Team Project*
