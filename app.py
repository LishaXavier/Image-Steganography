import io, streamlit as st
from PIL import Image
from stego import embed, extract
from crypto import encrypt, decrypt

st.title("🕵️ Image Steganography")
hide, reveal = st.tabs(["Hide", "Reveal"])

with hide:
    f = st.file_uploader("Cover image", type=["png", "jpg"], key="a")
    msg = st.text_area("Secret message")
    pw = st.text_input("Password (optional)", type="password", key="p1")
    if f and msg and st.button("Hide"):
        img = Image.open(f)
        st.caption(f"Capacity: {img.width*img.height*3//8 - 5} bytes")
        data = b"\x01" + encrypt(msg, pw) if pw else b"\x00" + msg.encode()
        try:
            out = embed(img, data)
            buf = io.BytesIO(); out.save(buf, "PNG")
            st.image(out)
            st.download_button("Download PNG", buf.getvalue(), "stego.png", "image/png")
        except ValueError as e:
            st.error(str(e))

with reveal:
    f2 = st.file_uploader("Stego PNG", type=["png"], key="b")
    pw2 = st.text_input("Password (if used)", type="password", key="p2")
    if f2 and st.button("Reveal"):
        try:
            data = extract(Image.open(f2))
            st.success(decrypt(data[1:], pw2) if data[0] else data[1:].decode())
        except Exception:
            st.error("Wrong password or no hidden message")