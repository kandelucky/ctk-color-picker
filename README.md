# ctk-color-picker

A modern, **Photoshop-style color picker dialog** for [CustomTkinter](https://github.com/TomSchimansky/CustomTkinter). One function call, one hex string back.

> Pure Python + Pillow. DPI-aware. Modal dialog. Works on Windows, macOS, Linux.

<p align="center">
  <img src="screenshots/picker.png" alt="Color picker dialog" width="280">
</p>

<p align="center">
  <img src="screenshots/demo.gif" alt="Color picker in action" width="520">
</p>

---

## Features

- 🎨 Saturation × Value square (drag to pick)
- 💡 HSL Lightness slider (black → color → white)
- 🌈 Hue slider
- 🔤 Hex input field
- 👀 Old / New comparison swatches
- 🎭 Tint strip — 13 dynamic variations of the current color
- 💾 Saved Colors — 20 slots, persistent across sessions (JSON)
- ⭐ Selection highlight on saved swatch matching current pick
- 🖥️ DPI-aware `tk.Canvas` — matches CTk widget scaling

## Requirements

| | |
|---|---|
| Python | **3.10+** |
| customtkinter | **5.2.2+** |
| Pillow | **10.0.0+** |

`tkinter` ships with Python on Windows/macOS. On Linux: `sudo apt install python3-tk`.

## Install

```bash
git clone https://github.com/kandelucky/ctk-color-picker.git
cd ctk-color-picker
pip install -e .
```

(`pip install -e .` installs the package in editable mode and pulls in `customtkinter` + `Pillow` automatically.)

> PyPI release coming soon: `pip install ctk-color-picker`

## Quick start

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

`askcolor()` opens the modal dialog, blocks until closed, and returns a hex string or `None` if cancelled.

<p align="center">
  <img src="screenshots/integration.png" alt="Picker integrated with an app" width="560">
</p>

---

## API

### `askcolor(master, initial="#1f6aa5", history=None, title="Color Picker") -> str | None`

Convenience function. Opens the dialog modally and returns the picked hex.

### `ColorPickerDialog(master, initial_color="#1f6aa5", history=None, title="Color Picker")`

The dialog class. Use directly when you need more control:

```python
dialog = ColorPickerDialog(parent, initial_color="#ff0000")
dialog.wait_window()
print(dialog.result)   # hex string or None
```

### `ColorHistory(path=None, max_entries=20)`

Manages persistent saved colors as a JSON file. Default path is `~/.ctk_color_picker/colors.json`. Pass to the dialog for custom storage.

```python
palette = ColorHistory(path="./project_palette.json", max_entries=30)
color = askcolor(app, history=palette)
```

Methods: `.add(hex)`, `.all()`, `.clear()`.

---

## Comparison

| | `tkinter.colorchooser` | `CTkColorPicker` (Akascape) | **`ctk-color-picker`** |
|---|---|---|---|
| Style | OS native | CTk wheel | **CTk + PIL** |
| Sat / Val square | ❌ | ❌ | ✅ |
| Hue slider | ❌ | ✅ | ✅ |
| Lightness slider | ❌ | ❌ | ✅ |
| Hex input | partial | ❌ | ✅ |
| Old / New swatches | ❌ | ❌ | ✅ |
| Tint strip | ❌ | ❌ | ✅ |
| Saved colors (persistent) | ❌ | ❌ | ✅ |
| DPI-aware canvas | n/a | partial | ✅ |

---

## Troubleshooting

**`ModuleNotFoundError: No module named 'ctk_color_picker'`** — run `pip install -e .` from the repo root, or copy the `ctk_color_picker/` folder next to your script.

**Dialog tiny / blurry on a 4K display** — make sure customtkinter ≥ 5.2.2.

**Saved colors don't persist** — check that `~/.ctk_color_picker/` is writable.

---

## License

[MIT](LICENSE) © 2026 kandelucky
