import numpy as np
from PIL import Image

def embed(img, data: bytes):
    arr = np.array(img.convert("RGB"))
    flat = arr.flatten()
    payload = len(data).to_bytes(4, "big") + data
    bits = np.unpackbits(np.frombuffer(payload, dtype=np.uint8))
    if len(bits) > len(flat):
        raise ValueError("Message too large for this image")
    flat[:len(bits)] = (flat[:len(bits)] & 254) | bits
    return Image.fromarray(flat.reshape(arr.shape))

def extract(img):
    flat = np.array(img.convert("RGB")).flatten()
    n = int.from_bytes(np.packbits(flat[:32] & 1).tobytes(), "big")
    if n * 8 > len(flat) - 32:
        raise ValueError("No hidden message")
    return np.packbits(flat[32:32 + n * 8] & 1).tobytes()