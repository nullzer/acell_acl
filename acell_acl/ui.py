from __future__ import annotations

import tkinter as tk
from tkinter import ttk

from acell_acl.model import (
    DEVELOPMENT_STAGES,
    SUPPORTED_PLATFORMS,
    AppState,
    ModeState,
    WorkMode,
    get_mode_status,
    set_network_resource_path,
    set_work_mode,
)


class LocalApp(tk.Tk):
    def __init__(self) -> None:
        super().__init__()
        self.title("Acell ACL")
        self.geometry("920x640")
        self.minsize(820, 560)
        self.configure(bg="#eef3fb")

        self.state_model = AppState()
        self.network_path = tk.StringVar()
        self.mode = tk.StringVar(value=WorkMode.LOCAL.value)

        self._configure_style()
        self._build_layout()
        self._refresh()

    def _configure_style(self) -> None:
        style = ttk.Style(self)
        style.theme_use("clam")
        style.configure("Root.TFrame", background="#eef3fb")
        style.configure("Card.TFrame", background="#ffffff", relief="flat")
        style.configure("Title.TLabel", background="#eef3fb", foreground="#102033", font=("Arial", 24, "bold"))
        style.configure("Subtitle.TLabel", background="#eef3fb", foreground="#45566f", font=("Arial", 11))
        style.configure("CardTitle.TLabel", background="#ffffff", foreground="#102033", font=("Arial", 14, "bold"))
        style.configure("Text.TLabel", background="#ffffff", foreground="#45566f", font=("Arial", 10))
        style.configure("Status.TLabel", background="#ffffff", foreground="#0f766e", font=("Arial", 13, "bold"))
        style.configure("Warning.TLabel", background="#ffffff", foreground="#b45309", font=("Arial", 13, "bold"))
        style.configure("Primary.TButton", font=("Arial", 10, "bold"), padding=(12, 8))
        style.configure("TEntry", fieldbackground="#ffffff", foreground="#102033", padding=8)

    def _build_layout(self) -> None:
        root = ttk.Frame(self, style="Root.TFrame", padding=24)
        root.pack(fill=tk.BOTH, expand=True)

        ttk.Label(root, text="Локальное Python-приложение", style="Title.TLabel").pack(anchor=tk.W)
        ttk.Label(
            root,
            text="Небольшое desktop-приложение для Windows 10 и ALT Linux с подготовкой к сборке.",
            style="Subtitle.TLabel",
        ).pack(anchor=tk.W, pady=(6, 22))

        content = ttk.Frame(root, style="Root.TFrame")
        content.pack(fill=tk.BOTH, expand=True)
        content.columnconfigure(0, weight=1)
        content.columnconfigure(1, weight=1)
        content.rowconfigure(1, weight=1)

        status_card = ttk.Frame(content, style="Card.TFrame", padding=20)
        status_card.grid(row=0, column=0, columnspan=2, sticky="ew", pady=(0, 16))
        status_card.columnconfigure(1, weight=1)

        ttk.Label(status_card, text="Режим работы", style="CardTitle.TLabel").grid(row=0, column=0, sticky=tk.W)
        modes = ttk.Frame(status_card, style="Card.TFrame")
        modes.grid(row=1, column=0, sticky=tk.W, pady=(12, 0))
        ttk.Radiobutton(modes, text="Локальный", value=WorkMode.LOCAL.value, variable=self.mode, command=self._change_mode).pack(
            side=tk.LEFT,
            padx=(0, 16),
        )
        ttk.Radiobutton(modes, text="Сетевой ресурс", value=WorkMode.NETWORK.value, variable=self.mode, command=self._change_mode).pack(
            side=tk.LEFT,
        )

        self.status_title = ttk.Label(status_card, style="Status.TLabel")
        self.status_title.grid(row=0, column=1, sticky=tk.E)
        self.status_details = ttk.Label(status_card, style="Text.TLabel", wraplength=440, justify=tk.RIGHT)
        self.status_details.grid(row=1, column=1, sticky=tk.E, pady=(12, 0))

        resource_card = ttk.Frame(content, style="Card.TFrame", padding=20)
        resource_card.grid(row=1, column=0, sticky="nsew", padx=(0, 8))
        resource_card.columnconfigure(0, weight=1)
        ttk.Label(resource_card, text="Сетевой ресурс", style="CardTitle.TLabel").pack(anchor=tk.W)
        ttk.Label(
            resource_card,
            text="Для многопользовательского режима укажите общий путь: \\\\server\\share, smb://server/share или /mnt/share.",
            style="Text.TLabel",
            wraplength=360,
        ).pack(anchor=tk.W, pady=(10, 14))
        self.network_entry = ttk.Entry(resource_card, textvariable=self.network_path)
        self.network_entry.pack(fill=tk.X)
        self.network_path.trace_add("write", self._change_network_path)

        platforms_card = ttk.Frame(content, style="Card.TFrame", padding=20)
        platforms_card.grid(row=1, column=1, sticky="nsew", padx=(8, 0))
        ttk.Label(platforms_card, text="Платформы запуска", style="CardTitle.TLabel").pack(anchor=tk.W)
        for platform in SUPPORTED_PLATFORMS:
            ttk.Label(platforms_card, text=f"✓ {platform.name}", style="CardTitle.TLabel").pack(anchor=tk.W, pady=(14, 0))
            ttk.Label(platforms_card, text=platform.description, style="Text.TLabel", wraplength=360).pack(anchor=tk.W)

        stages_card = ttk.Frame(root, style="Card.TFrame", padding=20)
        stages_card.pack(fill=tk.X, pady=(16, 0))
        ttk.Label(stages_card, text="Основные этапы разработки", style="CardTitle.TLabel").pack(anchor=tk.W)
        ttk.Label(stages_card, text=" → ".join(DEVELOPMENT_STAGES), style="Text.TLabel", wraplength=820).pack(anchor=tk.W, pady=(10, 0))

    def _change_mode(self) -> None:
        self.state_model = set_work_mode(self.state_model, WorkMode(self.mode.get()))
        self._refresh()

    def _change_network_path(self, *_args: object) -> None:
        self.state_model = set_network_resource_path(self.state_model, self.network_path.get())
        self._refresh()

    def _refresh(self) -> None:
        status = get_mode_status(self.state_model)
        self.status_title.configure(text=status.title)
        self.status_details.configure(text=status.details)

        if status.state is ModeState.NEEDS_NETWORK_RESOURCE:
            self.status_title.configure(style="Warning.TLabel")
        else:
            self.status_title.configure(style="Status.TLabel")

        if self.state_model.mode is WorkMode.LOCAL:
            self.network_entry.configure(state=tk.DISABLED)
        else:
            self.network_entry.configure(state=tk.NORMAL)


def run() -> None:
    app = LocalApp()
    app.mainloop()
