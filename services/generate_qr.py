import qrcode
import os

def generate_sample_qr(data="Product123-Serial456"):
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    output_path = os.path.join(project_root, "assets", "sample_qr.png")

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    img = qrcode.make(data)
    img.save(output_path)
