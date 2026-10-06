<div align="center">

# 🌙 Night Sky Companion

**A fully offline constellation spotter with open-source AI narration.**

*Point, look up, and let the universe introduce itself.*

[![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=flat&logo=python&logoColor=white)](https://python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.30+-FF4B4B?style=flat&logo=streamlit&logoColor=white)](https://streamlit.io)
[![Skyfield](https://img.shields.io/badge/Skyfield-1.46+-4A90D9?style=flat)](https://rhodesmill.org/skyfield)
[![Ollama](https://img.shields.io/badge/Ollama-gemma2:2b-000000?style=flat)](https://ollama.com)
[![License](https://img.shields.io/badge/License-MIT-green?style=flat)](LICENSE)

</div>

---

## 🌌 What It Is

Night Sky Companion tells you what's above your head **right now** — constellations, bright stars, moon phase — and narrates their mythology through a locally running open-weight language model.

No internet connection required. No API keys. No data leaves your device.

| Feature | Description |
|---|---|
| 🔭 **Offline Sky Scan** | Computes visible constellations from your lat/lon and the current time |
| 🌕 **Moon Phase** | Shows illumination % and stargazing advice |
| ⭐ **Bright Stars** | Lists the brightest stars above your horizon |
| 🔴 **Red-Light Mode** | Scotopic red palette preserves your night vision |
| 📴 **Pocket Mode** | Tells you to put your phone down and look up |
| 📔 **Sky Journal** | Saves your observing sessions locally |

---

## 📸 Screenshots

### Tonight's Sky
![Scan results](screenshots/02-scan-results.png)

### Red-Light Night Vision Mode
![Red light mode](screenshots/03-red-light.png)

### Sky Journal
![Journal](screenshots/04-journal.png)

---

## 🚀 Quick Start

### Prerequisites

- **Python 3.11+**
- **[Ollama](https://ollama.com)** (for local AI narration)

### Install

```bash
# Clone
git clone https://github.com/YOUR_USERNAME/night-sky-companion.git
cd night-sky-companion

# Create virtual environment
python -m venv .venv

# Activate it
# Windows (Git Bash):
source .venv/Scripts/activate
# macOS / Linux:
source .venv/bin/activate

# Install Python dependencies
pip install -r requirements.txt

# Pull the AI model (one-time, ~1.6 GB)
ollama pull gemma2:2b