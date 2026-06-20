from __future__ import annotations

from datetime import datetime, timezone
from typing import Any


# ── Country flag helpers ──────────────────────────────────────────────────────

COUNTRY_ISO: dict[str, str] = {
    "Argentina": "ar", "Brazil": "br", "France": "fr", "England": "gb-eng",
    "Germany": "de", "Spain": "es", "Portugal": "pt", "Netherlands": "nl",
    "Belgium": "be", "Uruguay": "uy", "Colombia": "co", "Mexico": "mx",
    "United States": "us", "USA": "us", "Canada": "ca", "Japan": "jp",
    "South Korea": "kr", "Morocco": "ma", "Senegal": "sn", "Ghana": "gh",
    "Nigeria": "ng", "Cameroon": "cm", "Australia": "au", "Saudi Arabia": "sa",
    "Iran": "ir", "Serbia": "rs", "Croatia": "hr", "Switzerland": "ch",
    "Denmark": "dk", "Poland": "pl", "Ecuador": "ec", "Chile": "cl",
    "Peru": "pe", "Venezuela": "ve", "Bolivia": "bo", "Paraguay": "py",
    "Costa Rica": "cr", "Panama": "pa", "Honduras": "hn", "El Salvador": "sv",
    "Jamaica": "jm", "Guatemala": "gt", "Algeria": "dz", "Egypt": "eg",
    "Tunisia": "tn", "South Africa": "za", "Ivory Coast": "ci",
    "Burkina Faso": "bf", "Mali": "ml", "Congo DR": "cd", "DR Congo": "cd",
    "Uganda": "ug", "Zimbabwe": "zw", "Zambia": "zm", "Angola": "ao",
    "Mozambique": "mz", "Tanzania": "tz", "Kenya": "ke", "New Zealand": "nz",
    "Fiji": "fj", "China PR": "cn", "China": "cn", "India": "in",
    "Thailand": "th", "Vietnam": "vn", "Iraq": "iq", "Jordan": "jo",
    "Uzbekistan": "uz", "Bahrain": "bh", "Turkey": "tr", "Ukraine": "ua",
    "Austria": "at", "Czech Republic": "cz", "Hungary": "hu", "Romania": "ro",
    "Slovakia": "sk", "Slovenia": "si", "Albania": "al",
    "North Macedonia": "mk", "Wales": "gb-wls", "Scotland": "gb-sct",
    "Greece": "gr", "Finland": "fi", "Norway": "no", "Sweden": "se",
    "Iceland": "is", "Qatar": "qa", "Cuba": "cu", "Haiti": "ht",
    "Trinidad and Tobago": "tt", "Curacao": "cw", "Guyana": "gy",
    "Suriname": "sr", "United Arab Emirates": "ae", "Libya": "ly",
    "Sudan": "sd", "Liberia": "lr", "Guinea": "gn", "Benin": "bj",
    "Cape Verde": "cv", "Ethiopia": "et", "Comoros": "km",
}

FLAG_EMOJI: dict[str, str] = {
    "Argentina": "🇦🇷", "Brazil": "🇧🇷", "France": "🇫🇷", "England": "🏴󠁧󠁢󠁥󠁮󠁧󠁿",
    "Germany": "🇩🇪", "Spain": "🇪🇸", "Portugal": "🇵🇹", "Netherlands": "🇳🇱",
    "Belgium": "🇧🇪", "Uruguay": "🇺🇾", "Colombia": "🇨🇴", "Mexico": "🇲🇽",
    "United States": "🇺🇸", "USA": "🇺🇸", "Canada": "🇨🇦", "Japan": "🇯🇵",
    "South Korea": "🇰🇷", "Morocco": "🇲🇦", "Senegal": "🇸🇳", "Ghana": "🇬🇭",
    "Nigeria": "🇳🇬", "Cameroon": "🇨🇲", "Australia": "🇦🇺", "Saudi Arabia": "🇸🇦",
    "Iran": "🇮🇷", "Serbia": "🇷🇸", "Croatia": "🇭🇷", "Switzerland": "🇨🇭",
    "Denmark": "🇩🇰", "Poland": "🇵🇱", "Ecuador": "🇪🇨", "Chile": "🇨🇱",
    "Peru": "🇵🇪", "Venezuela": "🇻🇪", "Bolivia": "🇧🇴", "Paraguay": "🇵🇾",
    "Costa Rica": "🇨🇷", "Panama": "🇵🇦", "Honduras": "🇭🇳", "El Salvador": "🇸🇻",
    "Jamaica": "🇯🇲", "Guatemala": "🇬🇹", "Algeria": "🇩🇿", "Egypt": "🇪🇬",
    "Tunisia": "🇹🇳", "South Africa": "🇿🇦", "Ivory Coast": "🇨🇮",
    "Burkina Faso": "🇧🇫", "Mali": "🇲🇱", "Congo DR": "🇨🇩",
    "New Zealand": "🇳🇿", "China PR": "🇨🇳", "Turkey": "🇹🇷", "Ukraine": "🇺🇦",
    "Austria": "🇦🇹", "Czech Republic": "🇨🇿", "Hungary": "🇭🇺",
    "Romania": "🇷🇴", "Wales": "🏴󠁧󠁢󠁷󠁬󠁳󠁿", "Scotland": "🏴󠁧󠁢󠁳󠁣󠁴󠁿", "Greece": "🇬🇷",
    "Norway": "🇳🇴", "Sweden": "🇸🇪", "Qatar": "🇶🇦", "Iraq": "🇮🇶",
    "Jordan": "🇯🇴", "Uzbekistan": "🇺🇿",
}


def flag_url(country_name: str, width: int = 40) -> str:
    cc = COUNTRY_ISO.get(country_name, "")
    if cc:
        return f"https://flagcdn.com/w{width}/{cc}.png"
    return ""


def flag_emoji(country_name: str) -> str:
    return FLAG_EMOJI.get(country_name, "🏳️")


# ── Fixture helpers ───────────────────────────────────────────────────────────

LIVE_STATUSES = {"1H", "2H", "ET", "BT", "P", "SUSP", "INT", "HT", "LIVE"}
FINISHED_STATUSES = {"FT", "AET", "PEN"}
UPCOMING_STATUSES = {"NS", "TBD", "PST", "CANC", "ABD", "AWD", "WO"}
KNOCKOUT_ROUNDS = {
    "Round of 32", "Round of 16", "Quarter-finals",
    "Semi-finals", "3rd Place Final", "Final",
}


def fixture_status(fix: dict) -> str:
    s = fix.get("fixture", {}).get("status", {}).get("short", "NS")
    if s in LIVE_STATUSES:
        return "live"
    if s in FINISHED_STATUSES:
        return "finished"
    return "upcoming"


def is_group_stage(fix: dict) -> bool:
    rnd = fix.get("league", {}).get("round", "")
    return "Group" in rnd or "group" in rnd


def round_label(fix: dict) -> str:
    return fix.get("league", {}).get("round", "—")


def fixture_datetime(fix: dict) -> datetime | None:
    ts = fix.get("fixture", {}).get("timestamp")
    if ts:
        return datetime.fromtimestamp(ts, tz=timezone.utc)
    return None


def score_str(fix: dict) -> str:
    g = fix.get("goals", {})
    h, a = g.get("home"), g.get("away")
    if h is None or a is None:
        return "— : —"
    return f"{h} : {a}"


def parse_fixtures(raw: list[dict]) -> dict:
    """Return structured dict with grouped, knockout, live and upcoming fixtures."""
    groups: dict[str, list] = {}
    knockout: dict[str, list] = {}
    live: list = []
    upcoming: list = []
    finished: list = []

    for fix in raw:
        status = fixture_status(fix)
        rnd = round_label(fix)

        if status == "live":
            live.append(fix)
        elif status == "upcoming":
            upcoming.append(fix)
        else:
            finished.append(fix)

        if is_group_stage(fix):
            groups.setdefault(rnd, []).append(fix)
        else:
            knockout.setdefault(rnd, []).append(fix)

    finished.sort(key=lambda x: x.get("fixture", {}).get("timestamp", 0), reverse=True)
    upcoming.sort(key=lambda x: x.get("fixture", {}).get("timestamp", 0))

    return {
        "all": raw,
        "by_round_group": groups,
        "by_round_knockout": knockout,
        "live": live,
        "upcoming": upcoming,
        "finished": finished,
    }


def parse_standings(raw: list[dict]) -> dict[str, list]:
    """Return {group_name: [team_row, ...]} from API standings response."""
    result: dict[str, list] = {}
    if not raw:
        return result
    league_data = raw[0].get("league", {})
    standings_list = league_data.get("standings", [])
    for group in standings_list:
        if not group:
            continue
        group_name = group[0].get("group", "Grupo ?")
        result[group_name] = group
    return result


def build_team_group_map(standings_by_group: dict[str, list]) -> dict[int, str]:
    """Map team_id -> group letter (e.g. 'Group A')."""
    mapping: dict[int, str] = {}
    for group_name, teams in standings_by_group.items():
        for t in teams:
            tid = t.get("team", {}).get("id")
            if tid:
                mapping[tid] = group_name
    return mapping


def enrich_fixtures_with_group(
    fixtures: list[dict], team_group_map: dict[int, str]
) -> list[dict]:
    """Attach 'computed_group' field to each group-stage fixture."""
    for fix in fixtures:
        home_id = fix.get("teams", {}).get("home", {}).get("id")
        computed = team_group_map.get(home_id, "")
        fix["computed_group"] = computed
    return fixtures


def fixtures_by_group(
    fixtures: list[dict], team_group_map: dict[int, str]
) -> dict[str, list]:
    groups: dict[str, list] = {}
    for fix in fixtures:
        if not is_group_stage(fix):
            continue
        home_id = fix.get("teams", {}).get("home", {}).get("id")
        grp = team_group_map.get(home_id, "Indefinido")
        groups.setdefault(grp, []).append(fix)
    for g in groups:
        groups[g].sort(key=lambda x: x.get("fixture", {}).get("timestamp", 0))
    return groups


# ── Statistics helpers ────────────────────────────────────────────────────────

def parse_statistics(stats_response: list[dict]) -> dict:
    """Return {home: {...}, away: {...}} with clean stat values."""
    if len(stats_response) < 2:
        return {}

    def extract(team_stats: dict) -> dict:
        result = {}
        for s in team_stats.get("statistics", []):
            key = s.get("type", "")
            val = s.get("value")
            result[key] = val
        result["_team"] = team_stats.get("team", {})
        return result

    return {"home": extract(stats_response[0]), "away": extract(stats_response[1])}


def parse_events(events_response: list[dict]) -> list[dict]:
    """Clean event list sorted by time."""
    cleaned = []
    for ev in events_response:
        cleaned.append({
            "time": ev.get("time", {}).get("elapsed", "?"),
            "extra": ev.get("time", {}).get("extra"),
            "team": ev.get("team", {}).get("name", ""),
            "team_id": ev.get("team", {}).get("id"),
            "player": ev.get("player", {}).get("name", ""),
            "assist": ev.get("assist", {}).get("name", ""),
            "type": ev.get("type", ""),
            "detail": ev.get("detail", ""),
        })
    cleaned.sort(key=lambda x: (x["time"] if isinstance(x["time"], int) else 0))
    return cleaned


# ── Summary stats ─────────────────────────────────────────────────────────────

def tournament_summary(fixtures: list[dict]) -> dict:
    total = len(fixtures)
    finished = sum(1 for f in fixtures if fixture_status(f) == "finished")
    live_count = sum(1 for f in fixtures if fixture_status(f) == "live")
    goals = 0
    teams: set[int] = set()
    for f in fixtures:
        g = f.get("goals", {})
        h, a = g.get("home"), g.get("away")
        if h is not None:
            goals += h
        if a is not None:
            goals += a
        teams.add(f.get("teams", {}).get("home", {}).get("id", 0))
        teams.add(f.get("teams", {}).get("away", {}).get("id", 0))
    teams.discard(0)
    return {
        "total_matches": total,
        "matches_played": finished,
        "live": live_count,
        "upcoming": total - finished - live_count,
        "total_goals": goals,
        "teams": len(teams),
        "avg_goals": round(goals / finished, 2) if finished else 0,
    }


ROUND_ORDER = [
    "Group Stage", "Round of 32", "Round of 16",
    "Quarter-finals", "Semi-finals", "3rd Place Final", "Final",
]


def knockout_round_order(rnd: str) -> int:
    for i, r in enumerate(ROUND_ORDER):
        if r.lower() in rnd.lower():
            return i
    return 99
