# NarrativeFlow - AI Story Co-Writer

NarrativeFlow is a local, AI-powered storytelling and writing assistant that uses Ollama to run large language models (like Llama 3) entirely on your machine.

## Prerequisites

Before running the application, you must install the following software:

1. **Python 3.10+**: Download from [python.org](https://www.python.org/downloads/)
2. **Ollama**: Download from [ollama.com](https://ollama.com/download)

## Setup Instructions

1. **Install and Start Ollama**
   After installing Ollama, open your terminal or command prompt and run:
   ```bash
   ollama run llama3
   ```
   *Note: This will download the Llama 3 model (approx 4.7GB). Keep this terminal window open so the Ollama server continues running in the background.*

2. **Set up the Python Environment**
   Open a new terminal window in the project directory where `app.py` is located, and create a virtual environment:
   ```bash
   python -m venv venv
   ```

3. **Activate the Virtual Environment**
   - **Windows:**
     ```cmd
     venv\Scripts\activate
     ```
   - **Mac/Linux:**
     ```bash
     source venv/bin/activate
     ```

4. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

## Running the Application

With the virtual environment activated and Ollama running in the background, start the application:

```bash
streamlit run app.py
```

This will automatically open the NarrativeFlow interface in your default web browser (usually at `http://localhost:8501`).

## Troubleshooting

- **"Cannot connect to Ollama"**: Ensure that the Ollama application is running in the background or run `ollama serve` in a separate terminal.
- **Missing Module Errors**: Ensure your virtual environment is activated (`venv\Scripts\activate`) before running standard setup and execution commands.
- **Database Reset**: A local SQLite database (`narrativeflow.db`) is automatically created on the first run. To reset the application state, delete the `narrativeflow.db` file and the `sessions/` folder.
