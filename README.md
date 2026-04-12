# ctk-color-picker

A Photoshop-style color picker for **CustomTkinter** with a saturation/value square, HSL lightness slider, hue slider, hex input, tint strip, and persistent saved colors.

> Drop-in modal dialog. One function call. Returns a hex string.

## Features

- **Saturation × Value square** with crosshair indicator (drag to pick)
- **HSL Lightness slider** — full black-to-color-to-white range
- **Hue slider** — full spectrum
- **Hex input** with validation
- **Old / New color comparison** swatches
- **Tint strip** — 13 dynamic swatches showing variations of the current color (centered Lightness range)
- **Saved Colors** — 20 slots in 2 rows, click to load, `+` button to save current
- **Persistent storage** for saved colors at `~/.ctk_color_picker/colors.json`
- **Selection highlight** on saved swatch matching the current color
- **DPI-aware** — scales `tk.Canvas` to match CustomTkinter's widget DPI scaling
- **Modal dialog** with Esc/X to cancel, OK to confirm
- No web/native dialog — pure CTk + Pillow rendering

## Install

```bash
pip install ctk-color-picker
```

Or from source:

```bash
git clone https://github.com/kandelucky/ctk-color-picker.git
cd ctk-color-picker
pip install -e .
```

## Quick start

```python
import customtkinter as ctk
from ctk_color_picker import askcolor

ctk.set_appearance_mode("dark")
app = ctk.CTk()
app.geometry("300x200")

def pick():
    color = askcolor(app, initial="#1f6aa5")
    if color:
        button.configure(fg_color=color)

button = ctk.CTkButton(app, text="Pick a color", command=pick)
button.pack(expand=True, padx=20, pady=20)

app.mainloop()
```

## API

### `askcolor(master, initial="#1f6aa5", history=None, title="Color Picker") -> str | None`

Convenience function. Opens the dialog modally and returns the picked hex color, or `None` if cancelled.

### `ColorPickerDialog(master, initial_color="#1f6aa5", history=None, title="Color Picker")`

Modal `CTkToplevel` dialog. Use directly if you need more control:

```python
from ctk_color_picker import ColorPickerDialog

dialog = ColorPickerDialog(master, initial_color="#ff0000")
dialog.wait_window()
hex_color = dialog.result  # str or None
```

### `ColorHistory(path=None, max_entries=20)`

Manages persistent saved colors as JSON. Pass to the dialog if you want a custom storage location or to share history across pickers.

```python
from ctk_color_picker import ColorHistory, askcolor

history = ColorHistory(path="./project_palette.json", max_entries=30)
color = askcolor(app, history=history)
print(history.all())   # list of recent colors
history.clear()        # remove all
```

## Comparison

|  | `tkinter.colorchooser` | `CTkColorPicker` (Akascape) | **`ctk-color-picker`** |
|---|---|---|---|
| Native or custom | OS dialog | CTk wheel | **CTk + PIL** |
| Sat / Val square | ❌ | ❌ | ✅ |
| Hue slider | ❌ | ✅ | ✅ |
| HSL Lightness slider | ❌ | ❌ | ✅ |
| Hex input | partial | ❌ | ✅ |
| Old / New comparison | ❌ | ❌ | ✅ |
| Tint strip (per-color) | ❌ | ❌ | ✅ |
| Saved colors | ❌ | ❌ | ✅ (persistent) |
| DPI-aware canvas | n/a | partial | ✅ |
| Returns | RGB tuple | hex | hex |

## Requirements

- Python 3.10+
- customtkinter >= 5.2.2
- Pillow >= 10.0.0

## License

MIT — see [LICENSE](LICENSE)
