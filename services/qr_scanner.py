from pyzbar.pyzbar import decode
from PIL import Image
from typing import Optional

class QRScanner:
    def decode_from_image(self, image_path: str) -> Optional[str]:
        try:
            image = Image.open(image_path)
            decoded_objects = decode(image)

            if not decoded_objects:
                return None

            return decoded_objects[0].data.decode("utf-8")
        except Exception as e:
            raise RuntimeError(f"Failed to decode QR: {e}")
