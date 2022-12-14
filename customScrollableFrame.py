import customtkinter as ctk
import tkinter as tk
from tkinter import ttk
class ScrollableFrame(ttk.Frame):
    def __init__(self, container, *args, **kwargs):
        super().__init__(container, *args, **kwargs)
        self.canvas = tk.Canvas(self, highlightthickness=0, bg='#2b2b2b', width=500, height=500)

        # self.scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.canvas.yview)

        self.scrollbar = ctk.CTkScrollbar(self, orientation="vertical",
                                          command=self.canvas.yview,
                                          bg_color = ('#dbdbdb', '#2b2b2b',)
                                        )

        self.scrollable_frame = ctk.CTkFrame(self.canvas, width=412, height=500)

        self.scrollable_frame.bind("<Configure>", lambda *args, **kwargs: self.canvas.configure(
            scrollregion=self.canvas.bbox("all")))

        self.bind_all("<MouseWheel>", self._on_mousewheel)
        self.bind("<Destroy>", lambda *args, **kwargs: self.unbind_all("<MouseWheel>"))

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.canvas.pack(side="left", fill="both", expand=True)

        self.scrollbar.pack(side="right", fill="y")

    def _on_mousewheel(self, event):
        self.canvas.yview_scroll(-1 * round(event.delta / 120), "units")