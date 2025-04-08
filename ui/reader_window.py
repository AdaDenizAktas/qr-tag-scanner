import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
from services.qr_scanner import QRScanner
import os
import cv2
from pyzbar.pyzbar import decode
import threading

def launch_reader_into(win):
    win.title("QR Reader")
    win.geometry("400x550")

    win.focus_force()

    # Image display placeholder
    qr_label = tk.Label(win)
    qr_label.pack(pady=10)

    # Status/result label
    result_var = tk.StringVar(value="Waiting for QR decoding...")
    result_label = tk.Label(win, textvariable=result_var, wraplength=380)
    result_label.pack(pady=10)

    def decode_from_file():
        default_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "assets")
        filepath = filedialog.askopenfilename(
            initialdir=default_dir,
            title="Select QR Image",
            filetypes=[("Image Files", "*.png *.jpg *.jpeg *.bmp")]
        )
        if not filepath:
            result_var.set("QR decoding process cancelled.")
            return

        try:
            img = Image.open(filepath)
            img = img.resize((200, 200))
            qr_img = ImageTk.PhotoImage(img)
            qr_label.config(image=qr_img)
            qr_label.image = qr_img

            scanner = QRScanner()
            decoded = scanner.decode_from_image(filepath)
            result_var.set(f"Decoded: {decoded}" if decoded else "No QR code found.")
        except Exception as e:
            result_var.set(f"Error: {e}")

    def read_from_camera():
        def camera_thread():
            cap = cv2.VideoCapture(0)
            if not cap.isOpened():
                result_var.set("Camera not accessible.")
                return

            decoded = None
            captured_frame = None

            while True:
                ret, frame = cap.read()
                if not ret:
                    break

                decoded_objs = decode(frame)
                for obj in decoded_objs:
                    decoded = obj.data.decode('utf-8')
                    captured_frame = frame.copy()

                    pts = obj.polygon
                    if len(pts) >= 4:
                        pts = pts[:4]
                        for i in range(4):
                            pt1 = pts[i]
                            pt2 = pts[(i + 1) % 4]
                            cv2.line(frame, pt1, pt2, (0, 255, 0), 2)
                        cv2.putText(frame, decoded, (pts[0][0], pts[0][1] - 10),
                                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

                cv2.imshow("QR Camera Reader", frame)

                key = cv2.waitKey(1) & 0xFF
                if decoded:
                    result_var.set(f"Decoded from camera: {decoded}")
                    break
                elif key == ord('q'):
                    result_var.set("QR decoding process cancelled.")
                    break
                elif cv2.getWindowProperty("QR Camera Reader", cv2.WND_PROP_VISIBLE) < 1:
                    result_var.set("QR decoding process cancelled.")
                    break

            cap.release()
            cv2.destroyAllWindows()

            if decoded and captured_frame is not None:
                win.after(0, lambda: show_camera_vs_generated_qr(captured_frame))

        threading.Thread(target=camera_thread, daemon=True).start()

    def show_camera_vs_generated_qr(captured_frame):
        from PIL import Image
        import tempfile

        comp_win = tk.Toplevel()
        comp_win.title("Comparison: Captured vs Generated")
        x = win.winfo_x()
        y = win.winfo_y()
        comp_win.geometry(f"420x240+{x}+{y}")

        temp_img_path = os.path.join(tempfile.gettempdir(), "captured_qr_temp.png")
        cv2.imwrite(temp_img_path, captured_frame)

        try:
            captured_img = Image.open(temp_img_path).resize((200, 200))
            captured_photo = ImageTk.PhotoImage(captured_img)
            label1 = tk.Label(comp_win, text="Captured QR")
            label1.pack()
            img_label1 = tk.Label(comp_win, image=captured_photo)
            img_label1.image = captured_photo
            img_label1.pack(side="left", padx=10)

            generated_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "assets", "sample_qr.png")
            generated_img = Image.open(generated_path).resize((200, 200))
            generated_photo = ImageTk.PhotoImage(generated_img)
            label2 = tk.Label(comp_win, text="Generated QR")
            label2.pack()
            img_label2 = tk.Label(comp_win, image=generated_photo)
            img_label2.image = generated_photo
            img_label2.pack(side="right", padx=10)

        except Exception as e:
            tk.Label(comp_win, text=f"Error displaying QR images: {e}", fg="red").pack()

    tk.Button(win, text="Decode from File", command=decode_from_file).pack(pady=5)
    tk.Button(win, text="Read from Camera", command=read_from_camera).pack(pady=5)
