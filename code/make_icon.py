# create_empty_favicon.py
import struct

# Minimal valid 1x1 transparent ICO file
ico_data = (
    b'\x00\x00'  # Reserved
    b'\x01\x00'  # Type (1 = ICO)
    b'\x01\x00'  # Number of images
    b'\x01\x01\x00\x00\x01\x00\x20\x00'  # Image directory entry
    b'\x30\x00\x00\x00'  # Size
    b'\x16\x00\x00\x00'  # Offset
    b'\x28\x00\x00\x00'  # DIB header size
    b'\x01\x00\x00\x00'  # Width
    b'\x02\x00\x00\x00'  # Height
    b'\x01\x00'          # Planes
    b'\x20\x00'          # Bits per pixel
    b'\x00\x00\x00\x00'  # Compression
    b'\x00\x00\x00\x00'  # Image size
    b'\x00\x00\x00\x00'  # X pixels per meter
    b'\x00\x00\x00\x00'  # Y pixels per meter
    b'\x00\x00\x00\x00'  # Colors used
    b'\x00\x00\x00\x00'  # Important colors
    b'\x00\x00\x00\x00'  # Pixel data (transparent)
    b'\x00\x00\x00\x00'  # AND mask
)

with open('../static/favicon.ico', 'wb') as f:
    f.write(ico_data)

print("Empty favicon.ico created!")
