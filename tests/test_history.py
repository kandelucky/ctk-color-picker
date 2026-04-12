import json

import pytest

from ctk_color_picker.history import ColorHistory


@pytest.fixture
def history_path(tmp_path):
    return str(tmp_path / "colors.json")


class TestBasic:
    def test_empty_initially(self, history_path):
        h = ColorHistory(path=history_path)
        assert h.all() == []

    def test_add_single(self, history_path):
        h = ColorHistory(path=history_path)
        h.add("#ff0000")
        assert h.all() == ["#ff0000"]

    def test_add_multiple_newest_first(self, history_path):
        h = ColorHistory(path=history_path)
        h.add("#ff0000")
        h.add("#00ff00")
        h.add("#0000ff")
        assert h.all() == ["#0000ff", "#00ff00", "#ff0000"]

    def test_empty_string_ignored(self, history_path):
        h = ColorHistory(path=history_path)
        h.add("")
        assert h.all() == []

    def test_none_ignored(self, history_path):
        h = ColorHistory(path=history_path)
        h.add(None)
        assert h.all() == []


class TestDeduplication:
    def test_duplicate_moves_to_front(self, history_path):
        h = ColorHistory(path=history_path)
        h.add("#ff0000")
        h.add("#00ff00")
        h.add("#0000ff")
        h.add("#ff0000")
        assert h.all() == ["#ff0000", "#0000ff", "#00ff00"]

    def test_case_insensitive_dedupe(self, history_path):
        h = ColorHistory(path=history_path)
        h.add("#FF0000")
        h.add("#ff0000")
        assert h.all() == ["#ff0000"]

    def test_stored_as_lowercase(self, history_path):
        h = ColorHistory(path=history_path)
        h.add("#ABCDEF")
        assert h.all() == ["#abcdef"]


class TestMaxCap:
    def test_custom_max(self, history_path):
        h = ColorHistory(path=history_path, max_entries=3)
        for i in range(5):
            h.add(f"#00000{i}")
        assert len(h.all()) == 3
        assert h.all() == ["#000004", "#000003", "#000002"]

    def test_default_max_is_20(self, history_path):
        h = ColorHistory(path=history_path)
        for i in range(25):
            h.add(f"#{i:06x}")
        assert len(h.all()) == 20


class TestPersistence:
    def test_save_and_load(self, history_path):
        h1 = ColorHistory(path=history_path)
        h1.add("#123456")
        h1.add("#abcdef")

        h2 = ColorHistory(path=history_path)
        assert h2.all() == ["#abcdef", "#123456"]

    def test_file_is_json_list(self, history_path):
        h = ColorHistory(path=history_path)
        h.add("#ff0000")
        h.add("#00ff00")

        with open(history_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        assert isinstance(data, list)
        assert "#ff0000" in data
        assert "#00ff00" in data

    def test_corrupt_file_starts_empty(self, tmp_path):
        path = tmp_path / "colors.json"
        path.write_text("not valid json")
        h = ColorHistory(path=str(path))
        assert h.all() == []

    def test_missing_file_starts_empty(self, tmp_path):
        h = ColorHistory(path=str(tmp_path / "nonexistent.json"))
        assert h.all() == []


class TestClear:
    def test_clear_empties(self, history_path):
        h = ColorHistory(path=history_path)
        h.add("#ff0000")
        h.add("#00ff00")
        h.clear()
        assert h.all() == []

    def test_clear_persists(self, history_path):
        h1 = ColorHistory(path=history_path)
        h1.add("#ff0000")
        h1.add("#00ff00")
        h1.clear()

        h2 = ColorHistory(path=history_path)
        assert h2.all() == []

    def test_clear_on_empty(self, history_path):
        h = ColorHistory(path=history_path)
        h.clear()
        assert h.all() == []


class TestIsolation:
    def test_all_returns_copy(self, history_path):
        h = ColorHistory(path=history_path)
        h.add("#ff0000")
        result = h.all()
        result.append("#999999")
        assert h.all() == ["#ff0000"]
