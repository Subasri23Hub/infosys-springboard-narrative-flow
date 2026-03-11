# config/settings.py — App-wide constants

OLLAMA_URL  = "http://localhost:11434/api/generate"
OLLAMA_TAGS = "http://localhost:11434/api/tags"

MODELS = ["llama3:latest", "mistral", "gemma", "codellama", "phi3", "llama2"]

LENGTH_MAP = {
    "Short":        150,
    "Medium":       300,
    "Long":         500,
    "Chapter Mode": 700,
}

PAGES = ["💬 Story Chat", "🗺 World Builder", "🔧 Writer Tools", "✏️ Split Editor"]

GENRES = ["Fantasy","Sci-Fi","Thriller","Romance","Mystery","Horror","Adventure","Historical"]
TONES  = ["Dramatic","Dark","Funny","Emotional","Inspirational","Mysterious","Suspenseful"]
STYLES = ["Descriptive","Simple English","Advanced","Poetic","Dialogue-heavy"]

PERSONALITIES = [
    "Brave","Intelligent","Shy","Aggressive","Mysterious",
    "Cunning","Empathetic","Reckless","Wise","Broken",
]

QUICK_STARTERS = [
    "Begin with a mysterious letter at midnight",
    "A forgotten kingdom stirs from slumber",
    "The last human wakes to silence",
    "Two rivals meet for the final time",
    "A secret buried for centuries resurfaces",
]
