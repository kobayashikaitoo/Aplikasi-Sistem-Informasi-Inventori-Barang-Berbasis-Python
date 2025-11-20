"""View untuk form login."""

import tkinter as tk
from tkinter import messagebox, ttk

class LoginView(tk.Frame):
    def __init__(self, master: tk.Tk, auth_controller: "AuthController", on_success) -> None:
        super().__init__(master)
        self.master = master
        self.auth_controller = auth_controller
        self.on_success = on_success
        self._build_ui()

    def _build_ui(self) -> None:
        self.master.title("Login - Sistem Informasi Inventori")
        self.master.geometry("360x220")
        self.master.resizable(False, False)

        self.columnconfigure(0, weight=1)

        title = ttk.Label(self, text="Inventori Toko", font=("Segoe UI", 16, "bold"))
        title.grid(row=0, column=0, pady=(20, 10))

        form = ttk.Frame(self)
        form.grid(row=1, column=0, padx=30, sticky="ew")
        form.columnconfigure(1, weight=1)

        ttk.Label(form, text="Username").grid(row=0, column=0, sticky="w", pady=5)
        self.username_var = tk.StringVar()
        username_entry = ttk.Entry(form, textvariable=self.username_var)
        username_entry.grid(row=0, column=1, sticky="ew", pady=5)
        username_entry.focus()

        ttk.Label(form, text="Password").grid(row=1, column=0, sticky="w", pady=5)
        self.password_var = tk.StringVar()
        password_entry = ttk.Entry(form, textvariable=self.password_var, show="*")
        password_entry.grid(row=1, column=1, sticky="ew", pady=5)
        password_entry.bind("<Return>", lambda _: self.submit())

        login_button = ttk.Button(self, text="Masuk", command=self.submit)
        login_button.grid(row=2, column=0, pady=20, ipadx=10)

        self.pack(fill="both", expand=True)

    def submit(self) -> None:
        username = self.username_var.get()
        password = self.password_var.get()
        success, user, message = self.auth_controller.login(username, password)
        if success:
            messagebox.showinfo("Informasi", message)
            self.on_success(user)
        else:
            messagebox.showerror("Gagal", message)

