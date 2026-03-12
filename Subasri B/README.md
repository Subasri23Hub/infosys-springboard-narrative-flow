# INKFORGE — Narrative Flow Story Co-Writer

> *An AI-powered fiction writing studio. Local. Private. Yours.*

<br>

---

## What is INKFORGE?

**INKFORGE** is a full-stack AI story co-writing application that lets writers collaborate with a large language model to craft, develop, and publish fiction — entirely on their own machine.

No cloud. No API keys. No subscription. Just you, your story, and the AI.

Built as part of the **Infosys Springboard — Narrative Flow** project by **Subasri B**.

<br>

---

## Features

### ✦ The Forge — AI Writing Workspace
- Real-time story generation with **live token-by-token streaming**
- **10 writing actions** — Continue, Enhance, Rewrite, Plot Twist, Dialogue, Describe, Foreshadow, Raise Stakes, Flashback, End Chapter
- **8 genres** — Fantasy, Sci-Fi, Thriller, Romance, Horror, Mystery, Historical, Literary
- **6 tones** — Cinematic, Lyrical, Dark & Gritty, Whimsical, Epic, Intimate
- **8 scene moods** — dynamically shapes the AI's emotional register per passage
- User's input of characters and world context for prose to be generated

### ✦ Book Viewer
- Dual-page open book spread — reads like a physical novel
- Automatic pagination to 16 lines per page
- Bold / Italic / Underline formatting toolbar
- Serif / Sans-serif font toggle
- Smooth page-turn transitions

### ✦ PDF Export
- A5 print-ready PDF with cover page, chapter headers, and drop caps
- Alternating page numbers
- Platform-aware font loading (Windows / macOS / Linux)

### ✦ Author's Workshop
| Tool | Description |
|------|-------------|
| Character Forge | Full psychological profile — backstory, motivation, fear, contradiction, speech pattern |
| World Architect | Complete world bible — power systems, social structure, locations, history |
| Plot Architect | Structured outline using 5 frameworks — Three Act, Hero's Journey, Save the Cat, Five Act, Kishōtenketsu |
| Dialogue Coach | Rewrites dialogue with subtext — characters never say exactly what they mean |
| Prose Doctor | Diagnoses weaknesses and rewrites as a master author would |
| Story Analyst | Editorial feedback on pacing, voice, show vs tell, tension, or overall quality |

### ✦ Story Compass
- Personal AI writing coach — answers any story or craft question
- 8 Quick Craft shortcuts — Overcome Block, Pacing Guide, Subtext, Show Don't Tell, and more

### ✦ Story History & User Management
- Per-user accounts with SHA-256 password hashing
- Auto-save after every generation
- Search, pin, archive, rename, delete, and share stories
- Full story history with metadata (genre, word count, date)

<br>

---

## Tech Stack

| Layer | Technology | Purpose |
|-------|-----------|---------|
| Web Framework | Streamlit | Application layout, state management, reactive UI |
| AI Engine | Ollama (llama3) | Local LLM inference — story generation and extraction |
| Styling | Custom CSS + JS | Ink/cream design system, animations, book viewer |
| PDF Export | ReportLab | A5 print-ready PDF generation |
| Authentication | Python hashlib + secrets | SHA-256 hashing, session tokens |
| Fonts | Google Fonts | Playfair Display, Crimson Pro, Cormorant Garamond, Space Mono |

<br>

---

## Project Structure

```
Subasri/
├── app.py                          # Main Streamlit application
├── ui_components.py                # All UI rendering, CSS, book viewer, PDF generator
├── story_engine.py                 # Prompt engineering, genre/tone/action configs, guardrails
├── auth.py                         # Authentication, session management, history I/O
└── docs/
    ├── Phase1_Streamlit & UI.docx         # Phase 1 — UI & Streamlit Documentation
    ├── Phase2_Olama Integration.docx      # Phase 2 — Ollama LLM Integration
    └── Phase3_The Guardrails.docx         # Phase 3 - The Guardrails
```

<br>

---

## Setup & Installation

### Prerequisites
- Python 3.10 or higher
- [Ollama](https://ollama.com) installed and running

### 1. Install Ollama & Pull Model
```bash
# macOS / Linux
curl -fsSL https://ollama.com/install.sh | sh

# Pull the recommended model
ollama pull llama3

# Start the Ollama service
ollama serve
```

### 2. Install Python Dependencies
```bash
pip install streamlit requests reportlab
```

### 3. Run INKFORGE
```bash
streamlit run app.py
```

Open your browser at `http://localhost:8501`

<br>

---

## How It Works

```
User Input (Write Zone)
        ↓
StoryEngine builds system prompt
  [genre + tone + POV + mood + characters + world context + action directive]
        ↓
HTTP POST → Ollama /api/chat (stream=True)
        ↓
NDJSON token stream → Streamlit live placeholder
        ↓
Full passage saved to story_blocks
        ↓
Auto-extraction → characters + world context updated
        ↓
Auto-save → user history JSON
```

<br>

---

## Guardrails

INKFORGE includes a content guardrail layer in `story_engine.py` that ensures Ollama stays focused on story-related content only. Any off-topic query — general knowledge, CV writing, coding help — is intercepted and redirected back to the writing task with a creative, in-character refusal.

```
Without guardrails → model answers anything freely
With guardrails    → model stays as your story co-writer, always
```

<br>

---

## Documentation

Full technical documentation is available in the `docs/` folder:

| Document | Contents |
|----------|---------|
| `Phase1_Streamlit & UI.docx` | Phase 1 — Complete UI and Streamlit implementation walkthrough |
| `Phase2_Olama Integration.docx` | Phase 2 — Ollama integration, prompt engineering, streaming architecture |
| `Phase3_The Guardrails.docx` | Live demo presenter script with timing cues and sample responses |

<br>

---

## Phases

| Phase | Status | Description |
|-------|--------|-------------|
| Phase 1 | ✅ Complete | Full Streamlit UI — layout, design system, book viewer, PDF export |
| Phase 2 | ✅ Complete | Ollama integration — streaming inference, prompt engineering, multi-task AI |
| Phase 3 | ✅ Complete | Guardrails — content safety layer, off-topic redirection |

<br>

---

## Author

**Subasri B**
Infosys Springboard — Narrative Flow Project
`github.com/Subasri23Hub`

<br>

---

*INKFORGE — Write like a novelist. Think like an architect. Ship like an engineer.*
