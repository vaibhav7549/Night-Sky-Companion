"""
ai_narrator.py — Local LLM narration using Ollama + Gemma.

Generates constellation mythology and human-readable
"where to look" directions. Fully offline.
"""

import ollama
import json
import os

# Load constellation data
DATA_FILE = os.path.join(os.path.dirname(__file__), "constellation_data.json")
with open(DATA_FILE, "r", encoding="utf-8") as f:
    CONSTELLATION_DATA = json.load(f)


def _azimuth_to_direction(azimuth):
    """Convert azimuth degrees to compass direction."""
    if 315 <= azimuth or azimuth < 45:
        return "north"
    elif 45 <= azimuth < 135:
        return "east"
    elif 135 <= azimuth < 225:
        return "south"
    else:
        return "west"


def narrate_constellation(abbreviation, altitude, azimuth):
    """
    Generate a warm, personal narration for a constellation.
    Always returns a dict with keys: name, abbreviation, myth, look_here,
    narration, altitude, azimuth, direction, season.
    """
    # Find the constellation by abbreviation
    info = None
    name = None
    for cname, cdata in CONSTELLATION_DATA.items():
        if cdata["abbreviation"] == abbreviation:
            info = cdata
            name = cname
            break

    direction = _azimuth_to_direction(azimuth)

    # --- Fallback if constellation not in our database ---
    if info is None:
        fallback_narration = (
            f"I see the constellation {abbreviation}. "
            f"It's about {altitude:.0f}° above the horizon, toward the {direction}. "
            f"Keep looking up."
        )
        return {
            "name": abbreviation,
            "abbreviation": abbreviation,
            "myth": "A constellation visible from your location right now.",
            "look_here": f"Look toward the {direction}, about {altitude:.0f}° above the horizon.",
            "narration": fallback_narration,
            "altitude": altitude,
            "azimuth": azimuth,
            "direction": direction,
            "season": "",
        }

    # --- Normal path: constellation found in database ---
    prompt = f"""You are a friendly stargazing guide. A person is outside at night, looking at the sky.

They can see the constellation {name} ({abbreviation}) about {altitude:.0f}° above the horizon, toward the {direction}.

Here is the mythology:
{info['myth']}

Here is where to look:
{info['look_here']}

Write a short, warm, 2-3 sentence narration that:
1. Tells them the name and one fascinating fact
2. Gives them the "look here" direction in a natural way
3. Ends with an encouraging note to keep looking up

Do not use bullet points. Write as if you're standing next to them."""

    try:
        response = ollama.chat(
            model="gemma2:2b",
            messages=[{"role": "user", "content": prompt}],
            options={"temperature": 0.7, "num_predict": 150},
        )
        narration = response["message"]["content"].strip()
    except Exception as e:
        # Fallback if Ollama isn't running
        narration = f"{info['myth']} {info['look_here']} Keep looking up."

    return {
        "name": name,
        "abbreviation": abbreviation,
        "myth": info["myth"],
        "look_here": info["look_here"],
        "narration": narration,
        "altitude": altitude,
        "azimuth": azimuth,
        "direction": direction,
        "season": info.get("season", ""),
    }


def get_moon_narration(moon_phase):
    """Generate a short narration for the moon phase."""
    pct = moon_phase["illumination_pct"]
    
    # Determine the stargazing advice ourselves (don't let the LLM get this wrong)
    if pct >= 70:
        advice = "Bright moonlight washes out faint stars — stick to the Moon, planets, and bright constellations tonight."
    elif pct >= 30:
        advice = "Moderate moonlight — good for bright stars and double stars, but faint galaxies will be tough."
    else:
        advice = "Dark skies tonight — perfect for faint deep-sky objects like galaxies, nebulae, and the Milky Way."

    prompt = f"""You are a stargazing guide. Tonight's moon is a {moon_phase['name']} at {pct}% illumination.

Here is the stargazing advice for tonight:
"{advice}"

Rewrite this in one short, warm, personal sentence (under 25 words). Keep the meaning exactly the same."""

    try:
        response = ollama.chat(
            model="gemma2:2b",
            messages=[{"role": "user", "content": prompt}],
            options={"temperature": 0.5, "num_predict": 60},
        )
        return response["message"]["content"].strip()
    except Exception:
        return advice