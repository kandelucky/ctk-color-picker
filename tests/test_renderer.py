import pytest

from ctk_color_picker.renderer import GradientRenderer
from ctk_color_picker.state import HsvState


class TestTintColorsShape:
    def test_count_matches(self):
        state = HsvState.from_hex("#ff0000")
        for n in [3, 5, 11, 13, 20]:
            colors = GradientRenderer.tint_colors(state, count=n)
            assert len(colors) == n

    def test_hex_format(self):
        state = HsvState.from_hex("#1f6aa5")
        colors = GradientRenderer.tint_colors(state, count=7)
        for c in colors:
            assert isinstance(c, str)
            assert c.startswith("#")
            assert len(c) == 7
            int(c[1:], 16)

    def test_lightest_first_darkest_last(self):
        state = HsvState.from_hex("#808080")
        colors = GradientRenderer.tint_colors(state, count=11)
        first_r = int(colors[0][1:3], 16)
        last_r = int(colors[-1][1:3], 16)
        assert first_r > last_r


class TestTintColorsRange:
    def test_white_extends_downward(self):
        state = HsvState.from_hex("#ffffff")
        colors = GradientRenderer.tint_colors(state, count=11, range_width=0.5)
        assert colors[0] == "#ffffff"
        last_byte = int(colors[-1][1:3], 16)
        assert 110 < last_byte < 150

    def test_black_extends_upward(self):
        state = HsvState.from_hex("#000000")
        colors = GradientRenderer.tint_colors(state, count=11, range_width=0.5)
        assert colors[-1] == "#000000"
        first_byte = int(colors[0][1:3], 16)
        assert 110 < first_byte < 150

    def test_mid_is_centered(self):
        state = HsvState.from_hex("#808080")
        colors = GradientRenderer.tint_colors(state, count=11, range_width=0.5)
        first_byte = int(colors[0][1:3], 16)
        last_byte = int(colors[-1][1:3], 16)
        assert first_byte > 140
        assert last_byte < 120


class TestTintColorsHue:
    def test_red_stays_reddish(self):
        state = HsvState.from_hex("#ff0000")
        colors = GradientRenderer.tint_colors(state, count=7)
        for c in colors:
            r = int(c[1:3], 16)
            g = int(c[3:5], 16)
            b = int(c[5:7], 16)
            assert r >= g
            assert r >= b

    def test_blue_stays_bluish(self):
        state = HsvState.from_hex("#0000ff")
        colors = GradientRenderer.tint_colors(state, count=7)
        for c in colors:
            r = int(c[1:3], 16)
            g = int(c[3:5], 16)
            b = int(c[5:7], 16)
            assert b >= r
            assert b >= g


class TestHueStrip:
    def test_creates_image(self):
        img = GradientRenderer.hue_strip(width=260, height=18)
        assert img.mode == "RGB"
        assert img.size == (260, 18)

    def test_left_is_red(self):
        img = GradientRenderer.hue_strip(width=100, height=10)
        r, g, b = img.getpixel((0, 5))
        assert r > 200
        assert g < 50
        assert b < 50


class TestLightnessStrip:
    def test_creates_image(self):
        state = HsvState.from_hex("#ff0000")
        img = GradientRenderer.lightness_strip(state, width=260, height=18)
        assert img.mode == "RGB"
        assert img.size == (260, 18)

    def test_left_is_black(self):
        state = HsvState.from_hex("#ff0000")
        img = GradientRenderer.lightness_strip(state, width=100, height=10)
        r, g, b = img.getpixel((0, 5))
        assert r < 20 and g < 20 and b < 20

    def test_right_is_white(self):
        state = HsvState.from_hex("#ff0000")
        img = GradientRenderer.lightness_strip(state, width=100, height=10)
        r, g, b = img.getpixel((99, 5))
        assert r > 230 and g > 230 and b > 230


class TestSvSquare:
    def test_creates_image(self):
        img = GradientRenderer.sv_square(
            hue=0.5, width=260, height=185,
            render_width=130, render_height=92,
        )
        assert img.mode == "RGB"
        assert img.size == (260, 185)

    def test_top_left_is_white(self):
        img = GradientRenderer.sv_square(
            hue=0.0, width=100, height=100,
            render_width=50, render_height=50,
        )
        r, g, b = img.getpixel((0, 0))
        assert r > 240 and g > 240 and b > 240

    def test_bottom_is_black(self):
        img = GradientRenderer.sv_square(
            hue=0.5, width=100, height=100,
            render_width=50, render_height=50,
        )
        r, g, b = img.getpixel((50, 99))
        assert r < 15 and g < 15 and b < 15
