import tkinter as tk
from tkinter import messagebox
import os
from services.generate_qr import generate_sample_qr
from ui.reader_window import launch_reader_into

class QRApp:
    def __init__(self, root):
        self.root = root
        self.root.title("QR Code Generator")
        self.root.geometry("400x300")

        # Product Number Entry
        tk.Label(root, text="Product Number:").pack()
        self.product_entry = tk.Entry(root, width=40)
        self.product_entry.pack(pady=5)

        # Serial Number Entry
        tk.Label(root, text="Serial Number:").pack()
        self.serial_entry = tk.Entry(root, width=40)
        self.serial_entry.pack(pady=5)

        # Generate Button
        tk.Button(root, text="Generate QR", command=self.generate_qr).pack(pady=10)

        # Open Reader Window Button
        tk.Button(root, text="Read QR", command=self.open_reader_window).pack(pady=5)

        # Status
        self.status = tk.StringVar()
        tk.Label(root, textvariable=self.status, fg="blue").pack(pady=10)

    def generate_qr(self):
        pn = self.product_entry.get().strip()
        sn = self.serial_entry.get().strip()
        if not pn or not sn:
            messagebox.showwarning("Input Required", "Both fields are required.")
            return

        combined_data = f"{pn}-{sn}"
        try:
            generate_sample_qr(data=combined_data)
            self.status.set("QR Code generated successfully.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate QR: {e}")

    def open_reader_window(self):
        self.root.withdraw()  # Hide current window

        reader_window = tk.Toplevel(self.root)
        reader_window.title("QR Reader")
        x = self.root.winfo_x()
        y = self.root.winfo_y()
        reader_window.geometry(f"400x550+{x}+{y}")

        def on_close():
            reader_window.destroy()
            self.root.deiconify()  # Restore main window

        reader_window.protocol("WM_DELETE_WINDOW", on_close)
        launch_reader_into(reader_window)

def launch_gui():
    root = tk.Tk()
    app = QRApp(root)
    root.mainloop()
