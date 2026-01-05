from tkinter import Canvas, Tk, Frame, Label

TITLE = "Dabynn's Pomodoro Timer"
LAVENDER = "#E6E0FF"
DARK_PURPLE = "#5B2A86"
DARK_PURPLE_HOVER = "#6A3C9C"
TEXT_COLOR = "white"
FONT_MAIN = ("DepartureMono Nerd Font", 32, "bold")
FONT_SUB = ("DepartureMono Nerd Font", 12)
FONT_BUTTON = ("DepartureMono Nerd Font", 13, "bold")



def _rounded_rect(canvas, x1, y1, x2, y2, r=12, **kwargs):
    # Draw a rounded rectangle using four arcs and four rectangles
    canvas.create_arc(x1, y1, x1 + 2 * r, y1 + 2 * r, start=90, extent=90, style="pieslice", **kwargs)
    canvas.create_arc(x2 - 2 * r, y1, x2, y1 + 2 * r, start=0, extent=90, style="pieslice", **kwargs)
    canvas.create_arc(x1, y2 - 2 * r, x1 + 2 * r, y2, start=180, extent=90, style="pieslice", **kwargs)
    canvas.create_arc(x2 - 2 * r, y2 - 2 * r, x2, y2, start=270, extent=90, style="pieslice", **kwargs)
    canvas.create_rectangle(x1 + r, y1, x2 - r, y2, **kwargs)
    canvas.create_rectangle(x1, y1 + r, x2, y2 - r, **kwargs)


class RoundedButton(Canvas):
    def __init__(self, master, text, command, width=120, height=44, radius=14, fill=DARK_PURPLE, hover_fill=DARK_PURPLE_HOVER):
        super().__init__(master, width=width, height=height, bg=LAVENDER, highlightthickness=0, bd=0)
        self.fill = fill
        self.hover_fill = hover_fill
        self.command = command
        self.radius = radius
        self.text = text
        self.bind("<Button-1>", lambda _: self.command())
        self.bind("<Enter>", self._on_enter)
        self.bind("<Leave>", self._on_leave)
        self._draw(fill)

    def _draw(self, fill):
        self.delete("all")
        _rounded_rect(self, 2, 2, int(self.cget("width")) - 2, int(self.cget("height")) - 2, r=self.radius, fill=fill, outline="")
        self.create_text(int(self.cget("width")) // 2, int(self.cget("height")) // 2, text=self.text, fill=TEXT_COLOR, font=FONT_BUTTON)

    def _on_enter(self, _event):
        self._draw(self.hover_fill)

    def _on_leave(self, _event):
        self._draw(self.fill)


def format_time(total_seconds: int) -> str:
    minutes = total_seconds // 60
    seconds = total_seconds % 60
    return f"{minutes:02d}:{seconds:02d}"


def main():
    root = Tk()
    root.title(TITLE)
    root.configure(bg=LAVENDER)
    root.resizable(False, False)

    state = {
        "remaining": 0,
        "running": False,
        "after_id": None,
    }

    def update_display():
        timer_value.config(text=format_time(state["remaining"]))

    def cancel_after():
        if state["after_id"]:
            root.after_cancel(state["after_id"])
            state["after_id"] = None

    def tick():
        if not state["running"]:
            return
        if state["remaining"] <= 0:
            state["running"] = False
            state["remaining"] = 0
            update_display()
            return
        state["remaining"] -= 1
        update_display()
        state["after_id"] = root.after(1000, tick)

    def start_timer():
        if state["remaining"] <= 0:
            return
        if state["running"]:
            return
        state["running"] = True
        tick()

    def stop_timer():
        state["running"] = False
        cancel_after()

    def clear_timer():
        state["running"] = False
        cancel_after()
        state["remaining"] = 0
        update_display()

    def add_minutes(minutes: int):
        state["remaining"] += minutes * 60
        update_display()

    # Layout
    header = Label(root, text=TITLE, bg=LAVENDER, fg=DARK_PURPLE, font=("DepartureMono Nerd Font", 18, "bold"))
    header.pack(pady=(16, 6))

    timer_value = Label(root, text=format_time(0), bg=LAVENDER, fg=DARK_PURPLE, font=FONT_MAIN)
    timer_value.pack(pady=(0, 16))

    subtext = Label(root, text="Tap a duration, then Start", bg=LAVENDER, fg=DARK_PURPLE, font=FONT_SUB)
    subtext.pack(pady=(0, 14))

    increments_frame = Frame(root, bg=LAVENDER)
    increments_frame.pack(pady=(0, 14))

    for mins in (5, 15, 30, 60):
        btn = RoundedButton(increments_frame, text=f"+{mins} min", command=lambda m=mins: add_minutes(m), width=110)
        btn.pack(side="left", padx=6)

    controls_frame = Frame(root, bg=LAVENDER)
    controls_frame.pack(pady=(0, 18))

    start_btn = RoundedButton(controls_frame, text="Start", command=start_timer, width=100)
    start_btn.pack(side="left", padx=6)

    stop_btn = RoundedButton(controls_frame, text="Stop", command=stop_timer, width=100, fill="#40235F", hover_fill="#4C2D74")
    stop_btn.pack(side="left", padx=6)

    clear_btn = RoundedButton(controls_frame, text="Clear", command=clear_timer, width=100, fill="#3A2B52", hover_fill="#4A3A67")
    clear_btn.pack(side="left", padx=6)

    update_display()
    root.mainloop()


if __name__ == "__main__":
    main()