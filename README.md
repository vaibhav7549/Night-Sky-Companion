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

![Night Sky Companion](screenshots/hero.png)

| Feature | Description |
|---|---|
| 🔭 **Offline Sky Scan** | Computes visible constellations from your lat/lon and the current time |
| 🌕 **Moon Phase** | Shows illumination % and stargazing advice |
| ⭐ **Bright Stars** | Lists the brightest stars above your horizon |
| 🔴 **Red-Light Mode** | Scotopic red palette preserves your night vision |
| 📴 **Pocket Mode** | Tells you to put your phone down and look up |
| 📔 **Sky Journal** | Saves your observing sessions locally |

---

## 🚀 Quick Start

### Prerequisites

- **Python 3.11+**
- **[Ollama](https://ollama.com)** (for local AI narration)

### Install

```bash
git clone https://github.com/vaibhav7549/Night-Sky-Companion.git
cd Night-Sky-Companion

python -m venv .venv

# Windows (Git Bash):
source .venv/Scripts/activate
# macOS / Linux:
source .venv/bin/activate

pip install -r requirements.txt
ollama pull gemma2:2b