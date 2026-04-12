# ctk-color-picker

A modern, **Photoshop-style color picker dialog** for [CustomTkinter](https://github.com/TomSchimansky/CustomTkinter) applications. Drop it into any CTk app with one function call and get back a hex color string.

> Pure Python + Pillow. No native dialogs. Works on Windows, macOS, Linux. DPI-aware.

---

## Table of contents

- [What is this?](#what-is-this)
- [Why use it?](#why-use-it)
- [Visual layout](#visual-layout)
- [Features](#features)
- [Requirements](#requirements)
- [Installation](#installation)
- [Quick start](#quick-start)
- [API reference](#api-reference)
- [Recipes](#recipes)
- [How it works](#how-it-works)
- [Comparison](#comparison)
- [Troubleshooting](#troubleshooting)
- [License](#license)

---

## What is this?

This package gives you a single, fully-featured **modal color picker dialog** that you can open from any CustomTkinter application. The user picks a color and you get a hex string back (like `"#1f6aa5"`), or `None` if they cancelled.

It looks and feels like a "real" graphics editor color picker — saturation/value square, hue slider, lightness slider, hex input, tint variations, saved colors palette — all rendered with CustomTkinter widgets and Pillow-generated gradient images.

It is **not** a replacement for `tkinter.colorchooser` (which uses the OS native dialog). It is a modern, themed alternative for apps where you want consistent CTk styling and richer functionality.

---

## Why use it?

| Need | Reason this picker fits |
|---|---|
| Consistent dark-theme UI in a CTk app | Native CTk widgets — no jarring system color dialog |
| Saved palette across sessions | Built-in `ColorHistory` with JSON persistence |
| Tint variations of a chosen base color | Built-in dynamic tint strip |
| Visual hex input | Hex field that round-trips with the picker state |
| Old vs new color comparison | Built-in side-by-side swatches |
| High-DPI Windows display | Auto-scales `tk.Canvas` to match CTk's widget scaling |
| One-liner API | `askcolor(parent)` returns the picked hex |

---

## Visual layout

When the dialog opens, you see (top to bottom):

```
+----------------------------------+
|  New [█████]   Old [█████]       |   <- comparison swatches
|                                  |
|  ████████████████████████████    |   <- tint strip (13 swatches)
|                                  |
|  +----------------------------+  |
|  |                            |  |
|  |   Saturation × Value       |  |   <- click + drag to pick
|  |                       o    |  |      (crosshair indicator)
|  |                            |  |
|  +----------------------------+  |
|                                  |
|  ████████████████████████████    |   <- HSL Lightness slider
|  ████████████████████████████    |   <- Hue slider
|                                  |
|  Hex [#1f6aa5________________ ]  |   <- editable hex input
|                                  |
|  SAVED COLORS              [+]   |   <- "+" saves current color
|  ▢ ▢ ▢ ▢ ▢ ▢ ▢ ▢ ▢ ▢              |   <- 10 slots (row 1)
|  ▢ ▢ ▢ ▢ ▢ ▢ ▢ ▢ ▢ ▢              |   <- 10 slots (row 2)
|                                  |
|  [          OK            ]      |
+----------------------------------+
```

- **Drag** in the SV square or on either slider to pick.
- **Click** any saved color or tint swatch to load it.
- **Type** a hex value in the input and press Enter.
- **Esc** or the window close button cancels.

---

## Features

- 🎨 **Saturation × Value square** with crosshair indicator (click + drag to pick)
- 💡 **HSL Lightness slider** — full black → color → white range, distinct from SV's value axis
- 🌈 **Hue slider** — full visible spectrum
- 🔤 **Hex input** with validation (`#RRGGBB`), Enter or focus-out to commit
- 👀 **Old / New comparison** — see your starting color next to the new one
- 🎭 **Tint strip** — 13 dynamic swatches showing variations of the current color (centered around current Lightness)
- 💾 **Saved Colors palette** — 20 slots in 2 rows of 10, persistent across sessions
- ⭐ **Selection highlight** — currently active color in saved row gets a white border
- 🖥️ **DPI-aware** — `tk.Canvas` is scaled to match CTk's widget DPI scaling, so layout doesn't break on high-DPI displays
- ⌨️ **Keyboard shortcuts** — `Esc` to cancel, click `OK` to confirm
- 📦 **Configurable** — custom storage path, max history size, custom title, custom history instance
- 🪶 **Lightweight** — only depends on `customtkinter` and `Pillow`

---

## Requirements

| Requirement | Minimum version |
|---|---|
| Python | **3.10** |
| customtkinter | **5.2.2** |
| Pillow | **10.0.0** |

> Tested on Python 3.10 – 3.14, Windows 10/11. Should work on macOS and Linux but Windows is the primary target.

---

## Installation

### From source (recommended for now)

```bash
git clone https://github.com/kandelucky/ctk-color-picker.git
cd ctk-color-picker
pip install -e .
```

The `-e` flag installs in **editable mode** — any changes to the source files take effect immediately, no reinstall needed.

### Manual (without `pip install`)

If you don't want to install at all, just copy the `ctk_color_picker/` folder into your project and import it directly:

```
your_project/
├── main.py
└── ctk_color_picker/
    ├── __init__.py
    ├── dialog.py
    └── history.py
```

```python
# main.py
from ctk_color_picker import askcolor
```

The examples in this repo use a small `sys.path` shim so they can run without `pip install`.

### From PyPI

> Not yet published. Coming soon.

```bash
pip install ctk-color-picker
```

---

## Quick start

The simplest possible usage:

```python
import customtkinter as ctk
from ctk_color_picker import askcolor

ctk.set_appearance_mode("dark")
app = ctk.CTk()
app.geometry("300x200")

def on_pick():
    color = askcolor(app, initial="#1f6aa5")
    if color:
        button.configure(fg_color=color)

button = ctk.CTkButton(app, text="Pick a color", command=on_pick)
button.pack(expand=True, padx=20, pady=20)

app.mainloop()
```

What happens:
1. User clicks the button.
2. `askcolor()` opens the modal picker dialog and **blocks** until the user closes it.
3. Returns the picked hex string (like `"#ff5733"`) or `None` if cancelled.
4. Your code uses the returned color.

That's the entire API for the common case. Three lines: import, call, use.

---

## API reference

### `askcolor(master, initial="#1f6aa5", history=None, title="Color Picker") -> str | None`

Convenience function. Opens a modal `ColorPickerDialog`, waits for it to close, and returns the result.

**Parameters:**

| Name | Type | Default | Description |
|---|---|---|---|
| `master` | `CTk` / `CTkToplevel` / `CTk*` widget | required | The parent window. Picker is centered on it and grabbed as modal. |
| `initial` | `str` | `"#1f6aa5"` | The initial color displayed when the dialog opens (also shown as "Old"). |
| `history` | `ColorHistory \| None` | `None` | Custom `ColorHistory` instance. If `None`, a default one (with default storage path) is used. |
| `title` | `str` | `"Color Picker"` | Window title for the dialog. |

**Returns:** `str` (hex like `"#1f6aa5"`) on OK, or `None` on Cancel / Esc / window close.

**Example:**

```python
from ctk_color_picker import askcolor

color = askcolor(my_app, initial="#ff0000", title="Pick foreground color")
if color is None:
    print("User cancelled")
else:
    print(f"Picked: {color}")
```

---

### `ColorPickerDialog(master, initial_color="#1f6aa5", history=None, title="Color Picker")`

The dialog class itself. Use this directly when you need to:
- Inspect the dialog state before/after.
- Bind extra logic.
- Manage the lifecycle yourself instead of waiting blocking-style.

It is a `CTkToplevel`, so all standard Toplevel methods are available.

**Constructor parameters:** same as `askcolor()` above (except no separate keyword names — they map 1:1, with `initial` → `initial_color`).

**Attributes:**

| Attribute | Type | Description |
|---|---|---|
| `result` | `str \| None` | After the dialog closes, contains the picked hex or `None` if cancelled. Read this in a callback or after `wait_window()`. |

**Example:**

```python
from ctk_color_picker import ColorPickerDialog

dialog = ColorPickerDialog(parent, initial_color="#ff0000")
dialog.wait_window()           # blocks until closed
print(dialog.result)           # "#ff0000" or None
```

You can also open the dialog without waiting (non-blocking) and read `result` in a callback bound to `<Destroy>`.

---

### `ColorHistory(path=None, max_entries=20)`

Manages the persistent saved-colors palette. Stores colors as a JSON array on disk.

**Parameters:**

| Name | Type | Default | Description |
|---|---|---|---|
| `path` | `str \| None` | `None` | Path to the JSON storage file. If `None`, uses `~/.ctk_color_picker/colors.json`. |
| `max_entries` | `int` | `20` | Maximum number of colors to retain. Oldest are dropped first. |

**Methods:**

| Method | Description |
|---|---|
| `add(color: str)` | Add a hex color to history. If it already exists, moves it to the front. Saves to disk immediately. |
| `all() -> list[str]` | Returns the current list of colors, most recent first. |
| `clear()` | Removes all saved colors. Saves the empty list to disk. |

**Example — separate palette per project:**

```python
from ctk_color_picker import ColorHistory, askcolor

# UI design palette stored in current working dir
ui_palette = ColorHistory(path="./ui_palette.json", max_entries=30)

# Background palette in a different file
bg_palette = ColorHistory(path="./bg_palette.json", max_entries=10)

def pick_ui():
    return askcolor(app, history=ui_palette, title="UI color")

def pick_bg():
    return askcolor(app, history=bg_palette, title="Background color")
```

Each picker remembers its own colors independently.

---

## Recipes

### Load the picker with the current widget color

```python
def edit_button_color():
    current = button.cget("fg_color")     # CTk-stored color
    if not isinstance(current, str):
        current = "#1f6aa5"                # fallback
    new = askcolor(app, initial=current)
    if new:
        button.configure(fg_color=new)
```

### Multiple picker buttons sharing one history

```python
shared = ColorHistory()  # default path

def pick_for(label, target):
    color = askcolor(app, initial=target.cget("fg_color"),
                     history=shared, title=label)
    if color:
        target.configure(fg_color=color)

ctk.CTkButton(app, text="FG", command=lambda: pick_for("FG", widget1)).pack()
ctk.CTkButton(app, text="BG", command=lambda: pick_for("BG", widget2)).pack()
```

Both buttons will see and add to the same saved-colors list.

### Reset saved colors

```python
from ctk_color_picker import ColorHistory

ColorHistory().clear()  # wipes default storage
```

### Project-local palette that doesn't pollute the user's home directory

```python
import os
from ctk_color_picker import ColorHistory, askcolor

# Store next to your project, in version control? Add to .gitignore.
HISTORY_PATH = os.path.join(os.path.dirname(__file__), ".palette.json")

palette = ColorHistory(path=HISTORY_PATH, max_entries=20)
color = askcolor(app, history=palette)
```

### Read the picked color via dialog instead of `askcolor()`

```python
dialog = ColorPickerDialog(app, initial_color="#1f6aa5", title="Choose")
dialog.wait_window()

if dialog.result:
    print("Picked", dialog.result)
else:
    print("Cancelled")
```

---

## How it works

A short technical overview for the curious:

**Color model:** state is kept in HSV (`hue`, `saturation`, `value` floats in `[0..1]`). The HSL lightness slider converts to/from HSL via `colorsys` on the fly. The hex output is computed from HSV.

**Gradient rendering:** the SV square, hue slider, and lightness slider are `tk.Canvas` widgets. Their gradient backgrounds are generated as PIL `Image` objects (HSV mode → RGB mode), wrapped in `ImageTk.PhotoImage`, and drawn via `canvas.create_image`. The SV square is rendered at half resolution (130×92) and bilinear-resized to the target — about 28 ms per redraw.

**DPI scaling:** CustomTkinter scales its own widgets automatically based on the OS scale factor (1.5× on a Windows 150% display, etc.). Plain `tk.Canvas` does **not**. To keep the canvas the same physical size as adjacent CTk widgets, the dialog reads `ctk.ScalingTracker.get_window_scaling(self)` and multiplies all canvas dimensions by it. Event handlers convert canvas pixel coordinates back to logical 0..1 ranges using the same scale.

**Saved colors:** persisted as a plain JSON array of hex strings. The default path is `~/.ctk_color_picker/colors.json`; the directory is created on first save. The `+` button saves the current pick; OK saves *and* returns. The current pick is highlighted in the row with a thicker white border.

**Tint strip:** for the current HSV color, the strip computes 13 colors at evenly-spaced HSL lightness values within a 0.5-wide window centered on the current lightness, clamped + shifted at the 0..1 edges. This gives a natural "lighter and darker variants of this color" feel.

---

## Comparison

| Feature | `tkinter.colorchooser` | `CTkColorPicker` (Akascape) | **`ctk-color-picker`** |
|---|---|---|---|
| Dialog style | OS native | Custom CTk | **Custom CTk + PIL** |
| Sat / Val 2D picker | ❌ | ❌ | ✅ |
| Hue slider | ❌ | ✅ | ✅ |
| HSL Lightness slider | ❌ | ❌ | ✅ |
| Hex input field | partial | ❌ | ✅ |
| Old vs New swatches | ❌ | ❌ | ✅ |
| Per-color tint strip | ❌ | ❌ | ✅ |
| Persistent saved colors | ❌ | ❌ | ✅ |
| DPI-aware canvas | n/a | partial | ✅ |
| Returns | RGB tuple | hex | hex |
| Theme | OS | CTk | CTk |

Use `tkinter.colorchooser` when you want the OS native picker. Use `CTkColorPicker` if you want the simplest possible CTk wheel. Use **this package** when you want the full graphics-editor experience inside a CTk app.

---

## Troubleshooting

### "ModuleNotFoundError: No module named 'ctk_color_picker'"

You're running a script that imports the package, but Python can't find it. Either:
- `pip install -e .` from the repo root, **or**
- copy the `ctk_color_picker/` folder next to your script, **or**
- add the project root to `sys.path` (the bundled examples do this).

### The dialog opens but everything is tiny / blurry on a 4K display

Make sure CustomTkinter is at version **5.2.2 or newer** — older versions had inconsistent DPI handling. The dialog auto-scales the canvases to match CTk's reported window scaling, so this should work out of the box.

### Saved colors don't persist across runs

Check that `~/.ctk_color_picker/` is writable. On Windows this expands to `C:\Users\<you>\.ctk_color_picker\`. If you've passed a custom `path=` to `ColorHistory`, verify that directory exists and is writable.

### Highlight on saved color sometimes doesn't appear

This was a bug in pre-0.1.0 versions caused by `int()` truncating float-to-byte conversions. Fixed in 0.1.0 by switching to `round()`. Make sure you're on the latest version.

### The + button used to flicker in early builds

Fixed by reusing existing slot widgets via `configure()` instead of destroying and recreating them on every save.

---

## License

[MIT](LICENSE) © 2026 kandelucky

Contributions and issues welcome at [github.com/kandelucky/ctk-color-picker](https://github.com/kandelucky/ctk-color-picker).
