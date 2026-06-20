import os
import requests
from typing import Any, Dict, Optional
from src.cache_manager import CacheManager

BASE_URL = "https://v3.football.api-sports.io"


class FootballAPI:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.headers = {"x-apisports-key": api_key}
        self.league_id = int(os.getenv("LEAGUE_ID", "1"))
        self.season = int(os.getenv("SEASON", "2026"))
        self.cache = CacheManager()

    # ── low-level ────────────────────────────────────────────────────────────

    def _get(
        self,
        endpoint: str,
        params: Dict[str, Any] | None = None,
        cache_key: str | None = None,
        ttl: int = 3600,
    ) -> Optional[Dict]:
        if cache_key:
            hit = self.cache.get(cache_key)
            if hit is not None:
                return hit

        url = f"{BASE_URL}/{endpoint}"
        try:
            r = requests.get(url, headers=self.headers, params=params, timeout=15)
            r.raise_for_status()
            data = r.json()
        except Exception:
            return None

        if cache_key:
            self.cache.set(cache_key, data, ttl)
        return data

    # ── public API ───────────────────────────────────────────────────────────

    def get_status(self) -> Optional[Dict]:
        """Check API account status / remaining requests."""
        return self._get("status", cache_key="status", ttl=300)

    def get_fixtures(self) -> Optional[Dict]:
        return self._get(
            "fixtures",
            params={"league": self.league_id, "season": self.season},
            cache_key=f"fixtures_{self.league_id}_{self.season}",
            ttl=1800,
        )

    def get_standings(self) -> Optional[Dict]:
        return self._get(
            "standings",
            params={"league": self.league_id, "season": self.season},
            cache_key=f"standings_{self.league_id}_{self.season}",
            ttl=1800,
        )

    def get_fixture_statistics(self, fixture_id: int) -> Optional[Dict]:
        return self._get(
            "fixtures/statistics",
            params={"fixture": fixture_id},
            cache_key=f"stats_{fixture_id}",
            ttl=86400,
        )

    def get_fixture_events(self, fixture_id: int) -> Optional[Dict]:
        return self._get(
            "fixtures/events",
            params={"fixture": fixture_id},
            cache_key=f"events_{fixture_id}",
            ttl=86400,
        )

    def get_fixture_lineups(self, fixture_id: int) -> Optional[Dict]:
        return self._get(
            "fixtures/lineups",
            params={"fixture": fixture_id},
            cache_key=f"lineups_{fixture_id}",
            ttl=86400,
        )

    def get_head_to_head(self, team1_id: int, team2_id: int, last: int = 5) -> Optional[Dict]:
        return self._get(
            "fixtures/headtohead",
            params={"h2h": f"{team1_id}-{team2_id}", "last": last},
            cache_key=f"h2h_{min(team1_id, team2_id)}_{max(team1_id, team2_id)}",
            ttl=86400,
        )

    def discover_league(self) -> list:
        """Search for World Cup 2026 league ID if the default (1) is wrong."""
        data = self._get(
            "leagues",
            params={"name": "FIFA World Cup", "season": self.season},
            cache_key=f"leagues_discover_{self.season}",
            ttl=86400,
        )
        if data and data.get("response"):
            return data["response"]
        return []
