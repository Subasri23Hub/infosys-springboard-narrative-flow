# NarrativeFlow – Interactive Story Co-Writer ✒️

NarrativeFlow is a premium, Streamlit-based AI storytelling application designed for creative writers and enthusiasts. It leverages local Large Language Models (LLMs) via Ollama to provide a seamless, immersive, and privacy-focused co-writing experience.

With dynamic cinematic backgrounds, glassmorphism UI elements, and advanced narrative guardrails, NarrativeFlow transforms the act of writing into an interactive journey.

---

## ✨ Core Features

### 🎨 Immersive Storytelling Environment
- **Dynamic Cinematic backgrounds**: The interface adapts to your story's genre (Fantasy, Sci-Fi, Mystery, Romance, Horror) with high-quality video loops and tailored color palettes.
- **Glassmorphism UI**: A sleek, modern design featuring translucent panels and smooth animations.
- **Skeleton Loading**: Visual feedback during AI generation for a premium "streaming" feel.

### 🧠 Advanced AI Collaboration
- **Context-Aware Co-Writing**: The AI maintains consistency by tracking story history, character profiles, and summaries.
- **Story Pitch Generator**: Stuck on page one? Generate a structured story pitch (title, setting, protagonist, conflict, twist) to kickstart your creativity.
- **Automatic Summarization**: For long stories, NarrativeFlow automatically compresses history into a narrative summary to keep the LLM focused and context-efficient.

### 🛡️ Smart Guardrails
- **Scope Control**: NarrativeFlow is a specialist. It includes a multi-stage validation layer to ensure the AI stays focused on storytelling, politely redirecting out-of-scope requests (e.g., coding, math).
- **Custom Directives**: Fine-tune the AI's behavior with specific instructions for tone, pacing, or style.

### 👤 Character Management
- **Persistent Profiles**: Define and manage your cast. Store character names, roles, personalities, and motivations to ensure narrative consistency across many chapters.

### 📑 Export & Persistence
- **Auto-Save**: Projects are saved locally as JSON files, allowing you to pick up exactly where you left off.
- **Prose-Only Export (TXT)**: Download a clean version of your story for further editing.
- **Manuscript-Quality PDF**: Generate a beautifully typeset PDF with title pages, headers, and professional formatting.

---

## 🛠️ Technical Stack

- **Frontend**: [Streamlit](https://streamlit.io/) with custom Vanilla CSS & HTML5 Video integration.
- **AI Backend**: [Ollama](https://ollama.com/) (running `llama3`).
- **Logic**: Python 3.8+ for state management and modular processing.
- **PDF Engine**: [FPDF2](https://github.com/PyFPDF/fpdf2) for high-quality manuscript generation.

---

## 📋 Prerequisites

Ensure you have the following installed:
- **Python 3.8+**
- **Ollama**: [Download here](https://ollama.com/download)

After installing Ollama, pull the default model:
```bash
ollama pull llama3
```

---

## ⚙️ Installation

1. **Clone the project:**
   ```bash
   git clone <repository-url>
   cd NarrativeFlow
   ```

2. **Environment Setup (Recommended):**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

---

## 🏃 How to Run

Launch the application using Streamlit:

```bash
streamlit run app.py
```

---

## 📂 Project Structure

- `app.py`: Main orchestrator and UI entry point.
- `modules/`:
  - `chat.py`: Handles message rendering and the generation flow.
  - `llm.py`: Interaction with Ollama, prompt engineering, and scope control.
  - `sidebar.py`: Project management, story settings, and character controls.
  - `utils.py`: Theming, session state, and file export logic.
- `assets/`: Custom CSS and static resources.
- `prompts/`: Structured text templates for system messages and validators.
- `.narrativeflow_saves/`: Local directory for project persistence (auto-created).

---

## 🚀 Future Scope

NarrativeFlow is evolving. Planned features include:

1. **Multi-Model Support**: Integration with other local backends (LM Studio) and cloud APIs (Gemini, Claude) for model comparison.
2. **Branching Narratives**: A "Choose Your Own Adventure" mode with visual story mapping.
3. **AI Image Generation**: Automatically generate character portraits or scene concept art using Stable Diffusion integration.
4. **Collaborative Writing**: Real-time collaborative sessions for multiple human writers.
5. **Advanced Worldbuilding tools**: Wiki-style databases for tracking locations, lore, and magic systems.

---

## 📄 License

This project is open-source. Feel free to use and modify it for your own creative writing needs!
