import tkinter as tk
from tkinter import messagebox
from database import get_user_by_username, hash_password
from main_app_window import MainApplication # Akan kita buat nanti

class LoginWindow:
    """Kelas untuk mengelola jendela Login aplikasi."""
    def __init__(self, master):
        self.master = master
        master.title("Login Sistem Inventori")
        master.geometry("300x200")
        master.resizable(False, False)
        
        # Variabel untuk menampung input
        self.username_var = tk.StringVar()
        self.password_var = tk.StringVar()
        
        self.create_widgets()

    def create_widgets(self):
        """Membangun elemen GUI untuk Login."""
        
        # Label dan Entry Username
        tk.Label(self.master, text="Username:", font=('Arial', 10)).pack(pady=(15, 0))
        tk.Entry(self.master, textvariable=self.username_var, width=25).pack(pady=5)
        
        # Label dan Entry Password
        tk.Label(self.master, text="Password:", font=('Arial', 10)).pack(pady=(5, 0))
        tk.Entry(self.master, textvariable=self.password_var, show="*", width=25).pack(pady=5)
        
        # Tombol Login
        tk.Button(self.master, text="LOGIN", command=self.attempt_login, width=15, 
                  bg='#4CAF50', fg='white', relief=tk.RAISED).pack(pady=10)

    def attempt_login(self):
        """Memproses upaya login."""
        username = self.username_var.get()
        password = self.password_var.get()
        
        if not username or not password:
            messagebox.showerror("Error", "Username dan Password harus diisi.")
            return

        # 1. Ambil data user dari database
        user = get_user_by_username(username)
        
        if user:
            # 2. Hash password input dan bandingkan
            hashed_input = hash_password(password)
            
            if hashed_input == user['password']:
                messagebox.showinfo("Sukses", f"Selamat datang, {user['level']}!")
                
                # Sembunyikan jendela login
                self.master.withdraw() 
                
                # 3. Buka jendela utama (Dashboard)
                root_main = tk.Toplevel(self.master)
                # Kirim level user ke jendela utama untuk kontrol hak akses
                MainApplication(root_main, user['level']) 
                
            else:
                messagebox.showerror("Error", "Password salah.")
        else:
            messagebox.showerror("Error", "Username tidak ditemukan.")

# Catatan: Kelas ini tidak akan dijalankan langsung, melainkan dipanggil dari main.py