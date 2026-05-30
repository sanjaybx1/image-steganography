"""
╔══════════════════════════════════════════════════════╗
║     AES + LSB Steganography — GUI Version            ║
║     Author : Sanjay G (@sanjaybx1)                   ║
╚══════════════════════════════════════════════════════╝
"""

import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import threading
from stego import encode, decode, check_capacity
import sys
import io


class StegoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("🔐 AES + LSB Steganography Tool — Sanjay G")
        self.root.geometry("700x600")
        self.root.configure(bg="#0D1117")
        self.root.resizable(False, False)

        self.cover_image = tk.StringVar()
        self.stego_image = tk.StringVar()
        self.output_image = tk.StringVar()
        self.password_enc = tk.StringVar()
        self.password_dec = tk.StringVar()

        self._build_ui()

    def _build_ui(self):
        # Title
        tk.Label(self.root, text="🔐 AES-256 + LSB Image Steganography",
                 font=("Courier New", 16, "bold"), fg="#00FF41", bg="#0D1117").pack(pady=15)
        tk.Label(self.root, text="by Sanjay G | github.com/sanjaybx1",
                 font=("Courier New", 9), fg="#555555", bg="#0D1117").pack()

        # Tabs
        style = ttk.Style()
        style.theme_use('default')
        style.configure("TNotebook", background="#0D1117", borderwidth=0)
        style.configure("TNotebook.Tab", background="#161B22", foreground="#00FF41",
                        font=("Courier New", 10, "bold"), padding=[15, 5])
        style.map("TNotebook.Tab", background=[("selected", "#0D1117")])

        tabs = ttk.Notebook(self.root)
        tabs.pack(fill='both', expand=True, padx=20, pady=10)

        self.enc_tab = tk.Frame(tabs, bg="#0D1117")
        self.dec_tab = tk.Frame(tabs, bg="#0D1117")
        tabs.add(self.enc_tab, text="  🔒 ENCODE  ")
        tabs.add(self.dec_tab, text="  🔓 DECODE  ")

        self._build_encode_tab()
        self._build_decode_tab()

        # Log output
        tk.Label(self.root, text="[ Terminal Output ]", font=("Courier New", 9),
                 fg="#555", bg="#0D1117").pack(anchor='w', padx=20)
        self.log = tk.Text(self.root, height=7, bg="#161B22", fg="#00FF41",
                           font=("Courier New", 9), bd=0, padx=10, pady=5)
        self.log.pack(fill='x', padx=20, pady=(0, 15))

    def _label(self, parent, text):
        tk.Label(parent, text=text, font=("Courier New", 10), fg="#CCCCCC",
                 bg="#0D1117", anchor='w').pack(fill='x', padx=20, pady=(10, 2))

    def _entry(self, parent, var, show=None):
        e = tk.Entry(parent, textvariable=var, bg="#161B22", fg="#FFFFFF",
                     font=("Courier New", 10), bd=0, insertbackground="#00FF41",
                     show=show)
        e.pack(fill='x', padx=20, ipady=6)
        return e

    def _button(self, parent, text, cmd, color="#00FF41"):
        tk.Button(parent, text=text, command=cmd, bg=color, fg="#0D1117",
                  font=("Courier New", 10, "bold"), bd=0, cursor="hand2",
                  activebackground="#00CC33").pack(pady=10, ipadx=20, ipady=6)

    def _browse(self, var, save=False):
        if save:
            path = filedialog.asksaveasfilename(defaultextension=".png",
                                                filetypes=[("PNG files", "*.png")])
        else:
            path = filedialog.askopenfilename(filetypes=[("Image files", "*.png *.jpg *.jpeg *.bmp")])
        if path:
            var.set(path)

    def _build_encode_tab(self):
        self._label(self.enc_tab, "📂 Cover Image (input):")
        f = tk.Frame(self.enc_tab, bg="#0D1117")
        f.pack(fill='x', padx=20)
        tk.Entry(f, textvariable=self.cover_image, bg="#161B22", fg="#FFF",
                 font=("Courier New", 9), bd=0).pack(side='left', fill='x', expand=True, ipady=5)
        tk.Button(f, text="Browse", command=lambda: self._browse(self.cover_image),
                  bg="#21262D", fg="#00FF41", font=("Courier New", 9), bd=0,
                  cursor="hand2").pack(side='left', padx=5)

        self._label(self.enc_tab, "💬 Secret Message:")
        self.message_box = tk.Text(self.enc_tab, height=4, bg="#161B22", fg="#FFFFFF",
                                   font=("Courier New", 10), bd=0, padx=8, pady=5,
                                   insertbackground="#00FF41")
        self.message_box.pack(fill='x', padx=20)

        self._label(self.enc_tab, "🔑 AES Password:")
        self._entry(self.enc_tab, self.password_enc, show="*")

        self._label(self.enc_tab, "💾 Output Stego Image (.png):")
        f2 = tk.Frame(self.enc_tab, bg="#0D1117")
        f2.pack(fill='x', padx=20)
        tk.Entry(f2, textvariable=self.output_image, bg="#161B22", fg="#FFF",
                 font=("Courier New", 9), bd=0).pack(side='left', fill='x', expand=True, ipady=5)
        tk.Button(f2, text="Browse", command=lambda: self._browse(self.output_image, save=True),
                  bg="#21262D", fg="#00FF41", font=("Courier New", 9), bd=0,
                  cursor="hand2").pack(side='left', padx=5)

        self._button(self.enc_tab, "🔒  ENCODE & HIDE MESSAGE", self._run_encode)

    def _build_decode_tab(self):
        self._label(self.dec_tab, "📂 Stego Image (with hidden message):")
        f = tk.Frame(self.dec_tab, bg="#0D1117")
        f.pack(fill='x', padx=20)
        tk.Entry(f, textvariable=self.stego_image, bg="#161B22", fg="#FFF",
                 font=("Courier New", 9), bd=0).pack(side='left', fill='x', expand=True, ipady=5)
        tk.Button(f, text="Browse", command=lambda: self._browse(self.stego_image),
                  bg="#21262D", fg="#00FF41", font=("Courier New", 9), bd=0,
                  cursor="hand2").pack(side='left', padx=5)

        self._label(self.dec_tab, "🔑 AES Password:")
        self._entry(self.dec_tab, self.password_dec, show="*")

        self._button(self.dec_tab, "🔓  EXTRACT & DECRYPT MESSAGE", self._run_decode, color="#FF6633")

        self._label(self.dec_tab, "📨 Extracted Message:")
        self.result_box = tk.Text(self.dec_tab, height=5, bg="#161B22", fg="#00FF41",
                                  font=("Courier New", 11), bd=0, padx=8, pady=5)
        self.result_box.pack(fill='x', padx=20)

    def _log(self, text):
        self.log.insert('end', text + "\n")
        self.log.see('end')

    def _run_encode(self):
        img = self.cover_image.get()
        msg = self.message_box.get("1.0", "end").strip()
        pwd = self.password_enc.get()
        out = self.output_image.get()

        if not all([img, msg, pwd, out]):
            messagebox.showerror("Missing Fields", "Please fill all fields.")
            return

        self._log(f"[*] Encoding message into: {img}")

        def task():
            try:
                old_stdout = sys.stdout
                sys.stdout = buffer = io.StringIO()
                encode(img, msg, pwd, out)
                sys.stdout = old_stdout
                self._log(buffer.getvalue())
                messagebox.showinfo("Success", f"Message hidden!\nSaved to: {out}")
            except Exception as e:
                sys.stdout = old_stdout
                self._log(f"[!] Error: {e}")
                messagebox.showerror("Error", str(e))

        threading.Thread(target=task, daemon=True).start()

    def _run_decode(self):
        img = self.stego_image.get()
        pwd = self.password_dec.get()

        if not all([img, pwd]):
            messagebox.showerror("Missing Fields", "Please select image and enter password.")
            return

        self._log(f"[*] Decoding from: {img}")

        def task():
            try:
                from stego import extract_lsb, aes_decrypt
                encrypted = extract_lsb(img)
                message = aes_decrypt(encrypted, pwd)
                self.result_box.delete("1.0", "end")
                self.result_box.insert("end", message)
                self._log("[✔] Message extracted and decrypted successfully!")
            except Exception as e:
                self._log(f"[!] Error: {e}")
                messagebox.showerror("Failed", "Wrong password or no hidden message found.")

        threading.Thread(target=task, daemon=True).start()


if __name__ == "__main__":
    root = tk.Tk()
    app = StegoApp(root)
    root.mainloop()
