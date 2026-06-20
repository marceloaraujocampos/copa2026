import json
import os
import time
from pathlib import Path
from typing import Any, Optional

CACHE_DIR = Path(__file__).parent.parent / "cache"


class CacheManager:
    def __init__(self):
        CACHE_DIR.mkdir(exist_ok=True)

    def _path(self, key: str) -> Path:
        safe = key.replace("/", "_").replace(":", "_").replace("?", "_").replace("&", "_")
        return CACHE_DIR / f"{safe}.json"

    def get(self, key: str) -> Optional[Any]:
        path = self._path(key)
        if not path.exists():
            return None
        try:
            with open(path, "r", encoding="utf-8") as f:
                envelope = json.load(f)
            if time.time() > envelope["expires_at"]:
                path.unlink(missing_ok=True)
                return None
            return envelope["data"]
        except (json.JSONDecodeError, KeyError, OSError):
            return None

    def set(self, key: str, value: Any, ttl: int = 3600) -> None:
        path = self._path(key)
        try:
            with open(path, "w", encoding="utf-8") as f:
                json.dump({"expires_at": time.time() + ttl, "data": value}, f)
        except OSError:
            pass

    def invalidate(self, key: str) -> None:
        self._path(key).unlink(missing_ok=True)

    def clear_all(self) -> None:
        for f in CACHE_DIR.glob("*.json"):
            f.unlink(missing_ok=True)

    def cache_info(self) -> dict:
        files = list(CACHE_DIR.glob("*.json"))
        valid = 0
        for f in files:
            try:
                with open(f) as fp:
                    e = json.load(fp)
                if time.time() < e.get("expires_at", 0):
                    valid += 1
            except Exception:
                pass
        return {"total": len(files), "valid": valid}
