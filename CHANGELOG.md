# Changelog

All notable changes to this project are documented here.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project follows [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.3.3] — 2026-04-25

### Fixed
- Bottom-edge clamp in `_center_on_parent` was using `winfo_width/height`
  on the dialog before it was mapped, so those calls returned `1x1` and
  the clamp let `y` fall low enough that the dialog actually extended
  below the screen / behind the taskbar. Two-phase clamp: skip the
  first attempt when dimensions are still `1x1`, then re-run via
  `after_idle` once the toplevel has rendered. Bottom reserve bumped
  60 → 80 px and a small 8 px margin added on the other edges.

## [0.3.2] — 2026-04-12

### Fixed
- Dialog could open partially below the screen edge when the parent
  window was near the bottom of the display. `_center_on_parent` now
  clamps the dialog to the visible screen area on all sides (with a
  60 px reserve for the taskbar), not just the top-left.

## [0.3.1] — 2026-04-12

### Fixed
- README images now use absolute GitHub raw URLs so they render on the
  PyPI project page (relative paths only worked on GitHub).

### Changed
- Install section now shows `pip install ctk-tint-color-picker` as the
  primary installation method.

## [0.3.0] — 2026-04-12

### Added
- Screen-wide **eyedropper** feature — click "💧 Pick" to sample any
  pixel on screen. Includes a live cursor-following preview bubble and
  a top-center hint toast with fade-out.
- `EyedropperController` — self-contained eyedropper module.
- `EyedropConfig` dataclass — tune preview size, overlay alpha, hint
  text, fade timing, and more.
- 68 unit tests covering `HsvState`, `ColorHistory`, and
  `GradientRenderer`.
- Docstrings on every public class and method.
- Module-level docstrings for each package file.

### Changed
- Extracted eyedropper logic from `dialog.py` into `eyedrop.py`,
  dropping `dialog.py` from 685 to ~500 lines.
- Explicit `PIL.Image.close()` on the screenshot after eyedrop to
  release the native buffer immediately.

## [0.2.0] — 2026-04-12

### Added
- Split `dialog.py` into focused modules: `state.py` (`HsvState`),
  `renderer.py` (`GradientRenderer`), and `config.py` (`PickerConfig`,
  `PickerTheme`).
- Dynamic tint strip — 13 swatches showing shades of the current color,
  centered on the current HSL lightness.
- HSL **Lightness slider** — separate control that extends past the
  sat/val square's darkness axis to true white.
- Clickable Old / New comparison swatches — click Old to revert.
- `Enter` key confirms OK.
- Selection highlight on the saved-colors row (white border on the
  swatch matching the current pick).

### Changed
- Default initial color is now white (`#ffffff`), was blue.
- `_build_ui` split into seven focused helper methods.
- Float → byte hex conversion uses `round()` instead of `int()` to keep
  hex round-trips precise.
- `GradientRenderer.sv_square` renders at half resolution and upscales
  with bilinear for ~2× speedup.

## [0.1.0] — Initial release

### Added
- `ColorPickerDialog` modal with saturation × value square, hue slider,
  hex input, and Old / New comparison swatches.
- `ColorHistory` persistent saved colors (JSON at
  `~/.ctk_color_picker/colors.json`).
- DPI-aware `tk.Canvas` — scales to match CustomTkinter's widget DPI.
- `askcolor()` convenience function.
