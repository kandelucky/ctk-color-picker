import pytest

from ctk_color_picker.state import HsvState


class TestHexRoundTrip:
    @pytest.mark.parametrize("hex_in", [
        "#1f6aa5", "#ff5733", "#abcdef", "#123456", "#888888",
        "#000000", "#ffffff",
        "#ff0000", "#00ff00", "#0000ff",
        "#ffff00", "#00ffff", "#ff00ff",
    ])
    def test_roundtrip(self, hex_in):
        state = HsvState.from_hex(hex_in)
        assert state.to_hex() == hex_in


class TestLoadHex:
    def test_valid_returns_true(self):
        state = HsvState()
        assert state.load_hex("#1f6aa5") is True

    def test_without_hash_prefix(self):
        state = HsvState()
        assert state.load_hex("ff0000") is True
        assert state.to_hex() == "#ff0000"

    def test_uppercase_input_normalized(self):
        state = HsvState()
        assert state.load_hex("#FF0000") is True
        assert state.to_hex() == "#ff0000"

    @pytest.mark.parametrize("bad", [
        "not a hex", "#12", "#1234", "#1234567",
        "#gggggg", "", None,
    ])
    def test_invalid_returns_false(self, bad):
        state = HsvState()
        state.load_hex("#1f6aa5")
        prev_hue = state.hue
        assert state.load_hex(bad) is False
        assert state.hue == prev_hue


class TestLightness:
    def test_white_is_1(self):
        state = HsvState.from_hex("#ffffff")
        assert abs(state.lightness() - 1.0) < 0.01

    def test_black_is_0(self):
        state = HsvState.from_hex("#000000")
        assert abs(state.lightness() - 0.0) < 0.01

    def test_pure_red_is_half(self):
        state = HsvState.from_hex("#ff0000")
        assert abs(state.lightness() - 0.5) < 0.01

    def test_mid_gray_is_half(self):
        state = HsvState.from_hex("#7f7f7f")
        assert abs(state.lightness() - 0.5) < 0.01

    def test_set_lightness_darker(self):
        state = HsvState.from_hex("#ff0000")
        state.set_lightness(0.25)
        assert state.lightness() < 0.5
        r, g, b = state.to_rgb()
        assert r >= g and r >= b

    def test_set_lightness_lighter(self):
        state = HsvState.from_hex("#ff0000")
        state.set_lightness(0.8)
        assert state.lightness() > 0.5

    def test_set_lightness_zero_is_black(self):
        state = HsvState.from_hex("#ff0000")
        state.set_lightness(0.0)
        assert state.to_hex() == "#000000"

    def test_set_lightness_one_is_white(self):
        state = HsvState.from_hex("#ff0000")
        state.set_lightness(1.0)
        assert state.to_hex() == "#ffffff"


class TestConversions:
    def test_to_rgb_range(self):
        for hex_in in ["#000000", "#ffffff", "#1f6aa5"]:
            state = HsvState.from_hex(hex_in)
            r, g, b = state.to_rgb()
            assert 0.0 <= r <= 1.0
            assert 0.0 <= g <= 1.0
            assert 0.0 <= b <= 1.0

    def test_to_hls_range(self):
        for hex_in in ["#000000", "#ffffff", "#1f6aa5", "#ff00ff"]:
            state = HsvState.from_hex(hex_in)
            h, l, s = state.to_hls()
            assert 0.0 <= h <= 1.0
            assert 0.0 <= l <= 1.0
            assert 0.0 <= s <= 1.0


class TestDefaultState:
    def test_default_is_black(self):
        state = HsvState()
        assert state.hue == 0.0
        assert state.saturation == 0.0
        assert state.value == 0.0
        assert state.to_hex() == "#000000"
