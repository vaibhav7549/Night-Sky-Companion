<div align="center">

# 🌙 Night Sky Companion

### *Your sky. Your AI. Your laptop. Nobody else's.*

A fully offline constellation spotter that runs **100% on your machine**.
Enter your location, press one button, and it tells you what's above your head
right now — constellations, bright stars, moon phase — narrated by an open-weight
LLM running locally.

**No internet. No API keys. No servers. No tracking.**

<br />

[![Python](https://img.shields.io/badge/Python-3.11%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://streamlit.io)
[![Skyfield](https://img.shields.io/badge/Skyfield-4A90D9?style=for-the-badge)](https://rhodesmill.org/skyfield)
[![Ollama](https://img.shields.io/badge/Ollama-000000?style=for-the-badge&logo=ollama&logoColor=white)](https://ollama.com)
[![Gemma 2](https://img.shields.io/badge/Gemma_2-4285F4?style=for-the-badge&logo=google&logoColor=white)](https://ai.google.dev/gemma)
[![License](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge)](LICENSE)
[![Made with Love](https://img.shields.io/badge/Made_with-❤️_for_the_night_sky-ff69b4?style=for-the-badge)](#)

<br />

[💡 Why](#-why-i-built-this) · [✨ Features](#-features) · [🎬 Demo](#-demo) · [🚀 Quick Start](#-quick-start) · [🕹️ How to Use](#%EF%B8%8F-how-to-use) · [🌍 Open AI](#-why-open-innovation-matters) · [🎃 Hacktoberfest](#-hacktoberfest-2026)

</div>

---

<div align="center">

## 💡 Why I Built This

</div>

> [!IMPORTANT]
> *"I'm standing on a ridge in the Himalayas.*
> *Zero cell signal. The Milky Way is so bright it casts shadows.*
> *I want to know what I'm looking at — but every app I have*
> *needs an internet connection to tell me."*
>
> — **Me, on a cold October night**

The best stargazing spots have no signal. That's the whole point of them — they're far from cities, far from light pollution, far from cell towers. But every astronomy app I tried wanted my location, my data, and a working internet connection just to name a star.

So I built something better.

**Night Sky Companion** gives you real astronomy, real mythology, and real "look here" directions with **zero internet required**. It uses an open-source astronomy library to compute star positions, an open-weight LLM to narrate them, and it does all of it on your laptop.

And then it tells you to **put your phone down and look up** — because that's the whole point.

This isn't an app that wants your attention. It's an app that wants to give it back.

---

<div align="center">

## ✨ Features

</div>

| &nbsp;&nbsp;🔭&nbsp;&nbsp; | **Offline Sky Scan** — Computes which constellations are overhead from your lat/lon, right now. |
|:---:|---|
| &nbsp;&nbsp;🌕&nbsp;&nbsp; | **Moon Phase** — Illumination % plus stargazing advice tuned to how dark the sky actually is. |
| &nbsp;&nbsp;⭐&nbsp;&nbsp; | **Bright Stars** — Lists the brightest stars above your horizon with altitude and compass direction. |
| &nbsp;&nbsp;🔴&nbsp;&nbsp; | **Red-Light Mode** — Scotopic red palette preserves your dark adaptation. A stargazing tradition. |
| &nbsp;&nbsp;📴&nbsp;&nbsp; | **Pocket Mode** — Actively tells you to stop looking at the screen. The sky will wait. |
| &nbsp;&nbsp;📔&nbsp;&nbsp; | **Sky Journal** — Logs every observing session locally. Your data stays with you. |
| &nbsp;&nbsp;🧠&nbsp;&nbsp; | **Open-Weight AI** — Gemma 2 narrates mythology and "look here" tips. Swap the model in one line. |
| &nbsp;&nbsp;🎨&nbsp;&nbsp; | **Glassmorphism UI** — Cinematic dark theme designed to be looked at *briefly* and then put away. |

---

<div align="center">

## 🎬 Demo

<img src="screenshots/hero.png" alt="Night Sky Companion demo" width="900" />

*Red-light mode active. 15 constellations detected, moon phase computed, Andromeda's mythology narrated — **fully offline**.*

</div>

---

<div align="center">

## 🧰 Tech Stack

| 🧩 Layer | 🛠️ Tool | 🎯 Purpose |
|:---:|:---:|:---|
| **Astronomy Engine** | [Skyfield](https://rhodesmill.org/skyfield) | Precise star, planet, and constellation positions |
| **Ephemeris** | [JPL DE421](https://naif.jpl.nasa.gov/pub/naif/generic_kernels/spk/planets/) | Bundled orbital data — no network needed |
| **Star Catalog** | [Hipparcos](https://en.wikipedia.org/wiki/Hipparcos) | 118,000 stars, public domain |
| **AI Runtime** | [Ollama](https://ollama.com) | Runs LLMs locally on any machine |
| **Model** | [Gemma 2 (2B)](https://ai.google.dev/gemma) | Google's open-weight model, Apache 2.0 |
| **UI** | [Streamlit](https://streamlit.io) | Instant web interface in pure Python |
| **Language** | [Python 3.11+](https://python.org) | Glues it all together |

</div>

---

<div align="center">

## 🚀 Quick Start

*From zero to stargazing in under 5 minutes.*

</div>

**1. Install Ollama** — [ollama.com/download](https://ollama.com/download)

**2. Download the model**
```bash
ollama pull gemma2:2b
