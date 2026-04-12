import json
import os

DEFAULT_MAX = 20


def _default_path() -> str:
    home = os.path.expanduser("~")
    folder = os.path.join(home, ".ctk_color_picker")
    os.makedirs(folder, exist_ok=True)
    return os.path.join(folder, "colors.json")


class ColorHistory:
    def __init__(self, path: str | None = None, max_entries: int = DEFAULT_MAX):
        self._path = path or _default_path()
        self._max = max_entries
        self._colors: list[str] = []
        self._loaded = False

    def _load(self) -> None:
        if self._loaded:
            return
        self._loaded = True
        try:
            with open(self._path, "r", encoding="utf-8") as f:
                data = json.load(f)
            if isinstance(data, list):
                self._colors = [c.lower() for c in data
                                if isinstance(c, str)][:self._max]
        except Exception:
            self._colors = []

    def _save(self) -> None:
        try:
            folder = os.path.dirname(self._path)
            if folder:
                os.makedirs(folder, exist_ok=True)
            with open(self._path, "w", encoding="utf-8") as f:
                json.dump(self._colors, f)
        except Exception:
            pass

    def add(self, color: str) -> None:
        if not color:
            return
        self._load()
        color = color.lower()
        if color in self._colors:
            self._colors.remove(color)
        self._colors.insert(0, color)
        self._colors = self._colors[:self._max]
        self._save()

    def all(self) -> list[str]:
        self._load()
        return list(self._colors)

    def clear(self) -> None:
        self._loaded = True
        self._colors = []
        self._save()
