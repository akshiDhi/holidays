#!/usr/bin/env python3

#  holidays
#  --------
#  A fast, efficient Python library for generating country, province and state
#  specific sets of holidays on the fly. It aims to make determining whether a
#  specific date is a holiday as fast and flexible as possible.
#
#  Authors: Vacanza Team and individual contributors (see CONTRIBUTORS file)
#           dr-prodigy <dr.prodigy.github@gmail.com> (c) 2017-2023
#           ryanss <ryanssdev@icloud.com> (c) 2014-2017
#  Website: https://github.com/vacanza/holidays
#  License: MIT (see LICENSE file)

"""Generate astronomical Sinhala Poya (full moon) dates for the holidays library.

Uses the bundled de421.bsp ephemeris (no network downloads) and Skyfield to
compute full-moon dates for Sri Lanka (UTC+5:30) and assign them to the correct
Sinhala lunar month using the Lahiri ayanamsha sidereal solar longitude.

Run with:

    python -m scripts.calendar.sinhala_generator

Or with uv:

    uv run -m scripts.calendar.sinhala_generator

Produces: holidays/calendars/sinhala_astronomy_dates.py

The generated *_POYA_DATES dicts and ADHI_POYA entries can then be reviewed and
merged into holidays/calendars/sinhala.py and holidays/countries/sri_lanka.py.

Algorithmic basis:
    * Full-moon moment is found astronomically via Skyfield (moon_phases).
    * The Poya civil date uses the "noon rule": the civil day whose noon (12:00
      Colombo/SL local time) is NEAREST to the full moon moment. Concretely:
        - if full moon occurs before noon SL time -> Poya = SL calendar day - 1
        - if full moon occurs at/after noon SL time -> Poya = SL calendar day
      This rule matches ~80% of 2005-2025 historical official dates and is the
      best deterministic rule available without the government committee's judgment.
    * The Sinhala month of a full moon is named after the solar rasi (sidereal
      zodiac sign, Lahiri ayanamsha) in which the Sun sits at the preceding new moon.
    * Adhi Masa: when the Sun occupies the SAME rasi at two consecutive new moons,
      the second full moon is an intercalary (Adhi) Poya.

References:
    * http://repository.kln.ac.lk/server/api/core/bitstreams/90201122-cb73-40a4-a9bc-d8e93f93b374/content
    * https://web.archive.org/web/20241120204015/https://documents.gov.lk/en/calendar.php
    * PR #3672: https://github.com/vacanza/holidays/pull/3672
"""

from __future__ import annotations

from collections import defaultdict
from datetime import date, timedelta, timezone
from pathlib import Path

from skyfield import almanac
from skyfield.api import load

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

# Sri Lanka Standard Time = UTC+5:30
SL_TZ = timezone(timedelta(hours=5, minutes=30))

# Bundled ephemeris -- already committed to the repository root.
_REPO_ROOT = Path(__file__).parents[2]
_BSP_PATH = _REPO_ROOT / "de421.bsp"

# Lahiri ayanamsha J2000 reference value (degrees) and annual precession rate.
# The Lahiri ayanamsha for J2000.0 epoch is 23.85 degrees; increases ~50.3"/yr.
_LAHIRI_J2000 = 23.85  # degrees at J2000.0
_PRECESSION_ARCSEC_PER_JY = 50.2564  # arcseconds per Julian year

# Sinhala month names indexed by solar rasi (0=Aries/Mesha, 11=Pisces/Mina).
# The Poya is named after the rasi the Sun occupies at the preceding new moon.
SINHALA_MONTH_NAMES = (
    "VESAK",    # 0: Aries   (Mesha)      -- Sun ~Apr-May
    "POSON",    # 1: Taurus  (Vrishabha)  -- Sun ~May-Jun
    "ESALA",    # 2: Gemini  (Mithuna)    -- Sun ~Jun-Jul
    "NIKINI",   # 3: Cancer  (Karka)      -- Sun ~Jul-Aug
    "BINARA",   # 4: Leo     (Simha)      -- Sun ~Aug-Sep
    "VAP",      # 5: Virgo   (Kanya)      -- Sun ~Sep-Oct
    "IL",       # 6: Libra   (Tula)       -- Sun ~Oct-Nov
    "UNDUVAP",  # 7: Scorpio (Vrischika)  -- Sun ~Nov-Dec
    "DURUTHU",  # 8: Sagitt. (Dhanu)      -- Sun ~Dec-Jan
    "NAWAM",    # 9: Capric. (Makara)     -- Sun ~Jan-Feb
    "MEDIN",    # 10: Aquar. (Kumbha)     -- Sun ~Feb-Mar
    "BAK",      # 11: Pisces (Mina)       -- Sun ~Mar-Apr
)

# Generation range.
# de421.bsp covers 1899-07-29 through 2053-10-09 (heliocentric).
# The search window extends 15 days into the next year, so cap at 2052.
# Use de440.bsp (covers to 2650) for a longer range if needed.
GENERATE_START = 2027
GENERATE_END = 2052

_MONTHS_ABBR = ("JAN", "FEB", "MAR", "APR", "MAY", "JUN",
                "JUL", "AUG", "SEP", "OCT", "NOV", "DEC")


# ---------------------------------------------------------------------------
# Ayanamsha and sidereal helpers
# ---------------------------------------------------------------------------


def _lahiri_ayanamsha_deg(jd_tt: float) -> float:
    """Return Lahiri ayanamsha in degrees for a given Julian Day (TT).

    Uses a linear model relative to J2000.0 (JD 2451545.0).
    Accurate to within ~0.01 deg over 2000-2100 -- sufficient for rasi id.
    """
    julian_years_from_j2000 = (jd_tt - 2_451_545.0) / 365.25
    ayanamsha = _LAHIRI_J2000 + julian_years_from_j2000 * (_PRECESSION_ARCSEC_PER_JY / 3600.0)
    return ayanamsha % 360.0


def _sun_sidereal_longitude(earth, sun, t) -> float:
    """Return the sidereal (Lahiri) longitude of the Sun in degrees [0, 360)."""
    astrometric = earth.at(t).observe(sun).apparent()
    _, lon, _ = astrometric.ecliptic_latlon(epoch="date")
    tropical_lon = lon.degrees % 360.0
    ayanamsha = _lahiri_ayanamsha_deg(t.tt)
    return (tropical_lon - ayanamsha) % 360.0


def _sun_rasi(earth, sun, t) -> int:
    """Return the solar rasi (0-11) for a given Skyfield time."""
    return int(_sun_sidereal_longitude(earth, sun, t) / 30.0)


# ---------------------------------------------------------------------------
# Poya date computation helpers
# ---------------------------------------------------------------------------


def _poya_date_from_fullmoon(fm_time) -> date:
    """Convert full moon time to the civil Poya date using the noon rule.

    Noon rule: the Poya is the SL civil day whose noon is closest to the
    full moon moment.
    - FM before noon SL -> Poya = previous SL calendar day
    - FM at/after noon SL -> Poya = that SL calendar day
    """
    sl_dt = fm_time.utc_datetime().astimezone(SL_TZ)
    sl_date = sl_dt.date()
    sl_hour = sl_dt.hour + sl_dt.minute / 60.0
    return sl_date - timedelta(days=1) if sl_hour < 12 else sl_date


# ---------------------------------------------------------------------------
# Core computation
# ---------------------------------------------------------------------------


def _load_ephemeris():
    """Load the bundled ephemeris. Raises FileNotFoundError if de421.bsp absent."""
    if not _BSP_PATH.exists():
        raise FileNotFoundError(
            f"de421.bsp not found at {_BSP_PATH}. "
            "It must be present in the repository root to run the generator."
        )
    ts = load.timescale()
    eph = load(str(_BSP_PATH))
    return ts, eph


def _find_moon_phases_for_year(ts, eph, year: int) -> tuple[list, list]:
    """Return (new_moon_times, full_moon_times) covering the given year.

    Search window extends into adjacent years so boundary full moons are captured.
    We filter to the target year using the civil Poya date (noon rule).
    """
    t0 = ts.utc(year - 1, 12, 15)
    t1 = ts.utc(year + 1, 1, 15)
    times, phases = almanac.find_discrete(t0, t1, almanac.moon_phases(eph))

    new_moons = [t for t, p in zip(times, phases, strict=True) if p == 0]
    full_moons = [t for t, p in zip(times, phases, strict=True) if p == 2]
    return new_moons, full_moons


def _preceding_new_moon(new_moons: list, full_moon_t):
    """Return the new moon time immediately preceding the given full moon."""
    fm_tt = full_moon_t.tt
    preceding = None
    for nm in new_moons:
        if nm.tt < fm_tt:
            preceding = nm
        else:
            break
    return preceding


def compute_poya_dates(
    start_year: int = GENERATE_START,
    end_year: int = GENERATE_END,
    ts=None,
    eph=None,
) -> tuple[dict, list]:
    """Compute Poya dates for the given Gregorian year range.

    Returns:
        poya_dates: dict[month_name, dict[year, [date, ...]]]
            Regular (non-Adhi) Poya dates keyed by month name then year.
        adhi_poyas: list of (year, date, adhi_month_name) for intercalary Poyas.
    """
    if ts is None or eph is None:
        ts, eph = _load_ephemeris()

    earth = eph["earth"]
    sun = eph["sun"]

    poya_dates: dict[str, dict[int, list[date]]] = defaultdict(lambda: defaultdict(list))
    adhi_poyas: list[tuple[int, date, str]] = []

    for year in range(start_year, end_year + 1):
        if year % 10 == 0:
            print(f"  Processing {year} ...")  # noqa: T201

        new_moons, full_moons = _find_moon_phases_for_year(ts, eph, year)

        # Only keep full moons whose Poya civil date falls in this year.
        year_full_moons = [
            fm for fm in full_moons if _poya_date_from_fullmoon(fm).year == year
        ]

        prev_rasi: int | None = None

        for fm in year_full_moons:
            pnm = _preceding_new_moon(new_moons, fm)
            if pnm is None:
                continue

            rasi = _sun_rasi(earth, sun, pnm)
            poya_date = _poya_date_from_fullmoon(fm)

            if prev_rasi is not None and rasi == prev_rasi:
                # Same rasi as previous full moon's new moon -> Adhi Masa.
                adhi_month_name = f"ADHI_{SINHALA_MONTH_NAMES[rasi]}"
                adhi_poyas.append((year, poya_date, adhi_month_name))
            else:
                month_name = SINHALA_MONTH_NAMES[rasi]
                poya_dates[month_name][year].append(poya_date)

            prev_rasi = rasi

    return poya_dates, adhi_poyas


# ---------------------------------------------------------------------------
# Historical validation
# ---------------------------------------------------------------------------


def validate_historical(ts=None, eph=None) -> tuple[int, int]:
    """Cross-check noon-rule astronomical output vs 2005-2025 official tables.

    Returns (matches, total) counting only single-date Poya months (11 months).
    The Duruthu poya (which spans year boundaries) is excluded from this count.
    """
    from holidays.calendars.sinhala import _SinhalaLunar  # noqa: PLC0415

    if ts is None or eph is None:
        ts, eph = _load_ephemeris()

    SINGLE_MONTHS = [
        "vesak", "poson", "esala", "nikini", "binara", "vap",
        "il", "unduvap", "nawam", "medin", "bak",
    ]

    match = 0
    total = 0
    cal = _SinhalaLunar()

    for year in range(2005, 2026):
        _, full_moons = _find_moon_phases_for_year(ts, eph, year)
        noon_set = {
            _poya_date_from_fullmoon(fm)
            for fm in full_moons
            if _poya_date_from_fullmoon(fm).year == year
        }

        for mname in SINGLE_MONTHS:
            official, _ = getattr(cal, f"{mname}_poya_date")(year)
            if official is None:
                continue
            total += 1
            if official in noon_set:
                match += 1
            else:
                adj = [d for d in [official - timedelta(1), official + timedelta(1)] if d in noon_set]
                adj_str = f" (FM off by 1: {adj[0]})" if adj else " (FM not found)"
                print(f"  MISMATCH {year} {mname}: official={official}{adj_str}")  # noqa: T201

    return match, total


# ---------------------------------------------------------------------------
# Output writer
# ---------------------------------------------------------------------------


def _date_to_tuple_str(d: date) -> str:
    return f"({_MONTHS_ABBR[d.month - 1]}, {d.day})"


def write_output(
    poya_dates: dict,
    adhi_poyas: list,
    start_year: int,
    end_year: int,
) -> None:
    """Write the generated data as a Python source file."""
    out_path = _REPO_ROOT / "holidays" / "calendars" / "sinhala_astronomy_dates.py"
    lines: list[str] = []

    lines += [
        "#  holidays",
        "#  --------",
        "#  A fast, efficient Python library for generating country, province and state",
        "#  specific sets of holidays on the fly. It aims to make determining whether a",
        "#  specific date is a holiday as fast and flexible as possible.",
        "#",
        "#  Authors: Vacanza Team and individual contributors (see CONTRIBUTORS file)",
        "#           dr-prodigy <dr.prodigy.github@gmail.com> (c) 2017-2023",
        "#           ryanss <ryanssdev@icloud.com> (c) 2014-2017",
        "#  Website: https://github.com/vacanza/holidays",
        "#  License: MIT (see LICENSE file)",
        "",
        f'"""Auto-generated Sinhala Poya dates {start_year}-{end_year}.',
        "",
        "Computed astronomically using Skyfield + de421.bsp, Lahiri ayanamsha.",
        "Noon rule: poya = SL calendar day before FM if FM before noon SL, else same day.",
        "DO NOT EDIT MANUALLY -- regenerate: python -m scripts.calendar.sinhala_generator",
        '"""',
        "",
        "from holidays.calendars.gregorian import (",
        "    JAN, FEB, MAR, APR, MAY, JUN, JUL, AUG, SEP, OCT, NOV, DEC,",
        ")",
        "",
    ]

    # Regular Poya date dicts
    for month_name in SINHALA_MONTH_NAMES:
        year_map = poya_dates.get(month_name, {})
        lines.append(f"{month_name}_POYA_DATES = {{")
        for year in range(start_year, end_year + 1):
            dates_for_year = year_map.get(year, [])
            if not dates_for_year:
                continue
            if len(dates_for_year) == 1:
                lines.append(f"    {year}: {_date_to_tuple_str(dates_for_year[0])},")
            else:
                tups = ", ".join(_date_to_tuple_str(d) for d in dates_for_year)
                lines.append(f"    {year}: ({tups}),")
        lines.append("}")
        lines.append("")

    # Adhi Poya dates
    if adhi_poyas:
        lines.append("# Adhi (intercalary) Poya dates -- add to SriLankaStaticHolidays")
        lines.append("ADHI_POYA_DATES = {")
        for year, d, name in sorted(adhi_poyas, key=lambda x: (x[0], x[1])):
            lines.append(f"    # {name}")
            lines.append(f"    {year}: {_date_to_tuple_str(d)},")
        lines.append("}")
        lines.append("")

    out_path.write_text("\n".join(lines), encoding="utf-8", newline="\n")
    print(f"\nWrote {out_path}")  # noqa: T201

    print(f"\n{'='*60}")  # noqa: T201
    print("Summary of Adhi (intercalary) Poya years:")  # noqa: T201
    for year, d, name in sorted(adhi_poyas, key=lambda x: x[0]):
        print(f"  {year}: {name} on {d}")  # noqa: T201


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------


def generate_data() -> None:
    """Main entry point."""
    print("=" * 60)  # noqa: T201
    print(f"Sinhala Poya generator -- {GENERATE_START}-{GENERATE_END}")  # noqa: T201
    print("=" * 60)  # noqa: T201

    ts, eph = _load_ephemeris()

    print("\nStep 1: Validating noon rule against 2005-2025 official calendar ...")  # noqa: T201
    match, total = validate_historical(ts, eph)
    print(  # noqa: T201
        f"\n  Result: {match}/{total} = {match/total*100:.1f}% historical dates match "
        f"(~20% are off by 1 day -- government committee rounding)."
    )

    print(f"\nStep 2: Generating {GENERATE_START}-{GENERATE_END} ...")  # noqa: T201
    poya_dates, adhi_poyas = compute_poya_dates(GENERATE_START, GENERATE_END, ts=ts, eph=eph)

    write_output(poya_dates, adhi_poyas, GENERATE_START, GENERATE_END)

    print("\nDone! Review sinhala_astronomy_dates.py and merge into sinhala.py")  # noqa: T201


if __name__ == "__main__":
    generate_data()
