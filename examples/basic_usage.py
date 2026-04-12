import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import customtkinter as ctk

from ctk_color_picker import askcolor


def main():
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")

    app = ctk.CTk()
    app.title("Color Picker — Basic Example")
    app.geometry("360x240")

    label = ctk.CTkLabel(app, text="No color picked yet", font=("", 13))
    label.pack(pady=(20, 10))

    swatch = ctk.CTkFrame(app, width=200, height=60,
                          fg_color="#ffffff",
                          border_width=1, border_color="#666666",
                          corner_radius=8)
    swatch.pack(pady=10)
    swatch.pack_propagate(False)

    def pick():
        current = label.cget("text").replace("Picked: ", "")
        if not current.startswith("#"):
            current = "#ffffff"
        color = askcolor(app, initial=current)
        if color:
            label.configure(text=f"Picked: {color}")
            swatch.configure(fg_color=color)

    ctk.CTkButton(app, text="Pick a color", command=pick,
                  width=180, height=36).pack(pady=10)

    app.mainloop()


if __name__ == "__main__":
    main()
