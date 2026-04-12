import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import customtkinter as ctk

from ctk_color_picker import ColorHistory, ColorPickerDialog


def main():
    ctk.set_appearance_mode("dark")

    app = ctk.CTk()
    app.title("Color Picker — Custom History Example")
    app.geometry("400x280")

    history = ColorHistory(path="./project_palette.json", max_entries=30)

    info = ctk.CTkLabel(
        app,
        text="History stored at ./project_palette.json\nMax 30 entries",
        font=("", 11),
    )
    info.pack(pady=(16, 8))

    swatch = ctk.CTkFrame(app, width=240, height=70,
                          fg_color="#1f6aa5",
                          border_width=1, border_color="#666666",
                          corner_radius=8)
    swatch.pack(pady=8)
    swatch.pack_propagate(False)

    def pick():
        dialog = ColorPickerDialog(
            app, initial_color="#1f6aa5", history=history,
            title="Project Palette",
        )
        dialog.wait_window()
        if dialog.result:
            swatch.configure(fg_color=dialog.result)
            print("Saved colors:", history.all())

    ctk.CTkButton(app, text="Open picker", command=pick,
                  width=200, height=36).pack(pady=8)

    ctk.CTkButton(app, text="Clear history",
                  command=history.clear, fg_color="#555555",
                  hover_color="#6a6a6a", width=200, height=30).pack(pady=4)

    app.mainloop()


if __name__ == "__main__":
    main()
