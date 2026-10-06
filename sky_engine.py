"""
sky_engine.py — Astronomy calculations using Skyfield.
Uses Skyfield's default cache directory (auto-managed).
"""

from skyfield.api import load, wgs84, Star
from skyfield.data import hipparcos
from skyfield.api import position_of_radec, load_constellation_map
from datetime import datetime, timezone
import numpy as np

_ts = None
_eph = None
_constellation_at = None
_hipparcos_stars = None


def _load_skyfield():
    """Lazy-load Skyfield objects once."""
    global _ts, _eph, _constellation_at, _hipparcos_stars

    if _ts is None:
        _ts = load.timescale()

    if _eph is None:
        _eph = load("de421.bsp")

    if _constellation_at is None:
        _constellation_at = load_constellation_map()

    if _hipparcos_stars is None:
        with load.open(hipparcos.URL) as f:
            _hipparcos_stars = hipparcos.load_dataframe(f)

    return _ts, _eph, _constellation_at, _hipparcos_stars


def get_visible_constellations(latitude, longitude, when=None):
    ts, eph, constellation_at, stars = _load_skyfield()

    if when is None:
        when = datetime.now(timezone.utc)

    t = ts.from_datetime(when)
    earth = eph["earth"]
    observer = earth + wgs84.latlon(latitude, longitude)

    bright = stars[stars["magnitude"] < 3.0].copy()
    results = {}

    for hip_id, star_row in bright.iterrows():
        ra_hours = star_row["ra_hours"]
        dec_degrees = star_row["dec_degrees"]
        star = Star(ra_hours=ra_hours, dec_degrees=dec_degrees)

        astrometric = observer.at(t).observe(star)
        alt, az, _ = astrometric.apparent().altaz()

        if alt.degrees > 0:
            pos = position_of_radec(ra_hours, dec_degrees)
            constellation = constellation_at(pos)

            if constellation not in results:
                results[constellation] = {
                    "abbreviation": constellation,
                    "altitude_max": alt.degrees,
                    "azimuth": az.degrees,
                    "star_count": 0,
                }
            else:
                if alt.degrees > results[constellation]["altitude_max"]:
                    results[constellation]["altitude_max"] = alt.degrees
                    results[constellation]["azimuth"] = az.degrees
            results[constellation]["star_count"] += 1

    sorted_results = sorted(
        results.values(), key=lambda x: x["altitude_max"], reverse=True
    )
    return sorted_results[:15]


def get_moon_phase(when=None):
    ts, eph, _, _ = _load_skyfield()

    if when is None:
        when = datetime.now(timezone.utc)

    t = ts.from_datetime(when)
    moon = eph["moon"]
    earth = eph["earth"]
    sun = eph["sun"]

    astrometric = earth.at(t).observe(moon)
    apparent = astrometric.apparent()
    phase_angle = apparent.phase_angle(sun).degrees
    phase_fraction = (1 + np.cos(np.radians(phase_angle))) / 2

    if phase_fraction < 0.1:
        name = "New Moon"
    elif phase_fraction < 0.4:
        name = "Waxing Crescent"
    elif phase_fraction < 0.6:
        name = "First Quarter"
    elif phase_fraction < 0.9:
        name = "Waxing Gibbous"
    elif phase_fraction < 0.95:
        name = "Full Moon"
    else:
        name = "Waning Gibbous"

    return {
        "fraction": round(phase_fraction, 3),
        "name": name,
        "illumination_pct": round(phase_fraction * 100, 1),
    }


def get_bright_stars(latitude, longitude, when=None, limit=10):
    ts, eph, constellation_at, stars = _load_skyfield()

    if when is None:
        when = datetime.now(timezone.utc)

    t = ts.from_datetime(when)
    earth = eph["earth"]
    observer = earth + wgs84.latlon(latitude, longitude)

    bright = stars[stars["magnitude"] < 1.5].copy()
    results = []

    for hip_id, star_row in bright.iterrows():
        ra_hours = star_row["ra_hours"]
        dec_degrees = star_row["dec_degrees"]
        star = Star(ra_hours=ra_hours, dec_degrees=dec_degrees)

        astrometric = observer.at(t).observe(star)
        alt, az, _ = astrometric.apparent().altaz()

        if alt.degrees > 5:
            pos = position_of_radec(ra_hours, dec_degrees)
            constellation = constellation_at(pos)
            results.append({
                "hip_id": int(hip_id),
                "magnitude": float(star_row["magnitude"]),
                "altitude": round(alt.degrees, 1),
                "azimuth": round(az.degrees, 1),
                "constellation": constellation,
            })

    results.sort(key=lambda x: x["magnitude"])
    return results[:limit]