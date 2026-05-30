"""
╔══════════════════════════════════════════════════════╗
║       AES + LSB Image Steganography Tool             ║
║       Author : Sanjay G (@sanjaybx1)                 ║
║       Tech   : AES-256 Encryption + LSB Embedding    ║
╚══════════════════════════════════════════════════════╝
"""

import os
import sys
import hashlib
import argparse
from PIL import Image
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes
import base64


# ─────────────────────────────────────────
#  AES ENCRYPTION / DECRYPTION
# ─────────────────────────────────────────

def derive_key(password: str) -> bytes:
    """Derive a 256-bit AES key from a password using SHA-256."""
    return hashlib.sha256(password.encode()).digest()


def aes_encrypt(message: str, password: str) -> bytes:
    """Encrypt message using AES-256 CBC mode."""
    key = derive_key(password)
    iv = get_random_bytes(16)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    encrypted = cipher.encrypt(pad(message.encode(), AES.block_size))
    # Prepend IV to ciphertext for use during decryption
    return iv + encrypted


def aes_decrypt(encrypted_data: bytes, password: str) -> str:
    """Decrypt AES-256 CBC encrypted bytes."""
    key = derive_key(password)
    iv = encrypted_data[:16]
    ciphertext = encrypted_data[16:]
    cipher = AES.new(key, AES.MODE_CBC, iv)
    decrypted = unpad(cipher.decrypt(ciphertext), AES.block_size)
    return decrypted.decode()


# ─────────────────────────────────────────
#  LSB ENCODING / DECODING
# ─────────────────────────────────────────

DELIMITER = "$$END$$"


def bytes_to_bits(data: bytes) -> str:
    """Convert bytes to a binary string."""
    return ''.join(format(byte, '08b') for byte in data)


def bits_to_bytes(bits: str) -> bytes:
    """Convert binary string back to bytes."""
    byte_array = bytearray()
    for i in range(0, len(bits), 8):
        byte_array.append(int(bits[i:i+8], 2))
    return bytes(byte_array)


def embed_lsb(image_path: str, data: bytes, output_path: str):
    """
    Hide encrypted bytes inside an image using LSB steganography.
    Modifies the least significant bit of each color channel.
    """
    img = Image.open(image_path).convert('RGB')
    pixels = list(img.getdata())

    # Encode data as base64 string + delimiter for extraction
    payload = base64.b64encode(data).decode() + DELIMITER
    bits = bytes_to_bits(payload.encode())

    max_bits = len(pixels) * 3
    if len(bits) > max_bits:
        print(f"[!] Error: Image too small. Need {len(bits)} bits, image has {max_bits} bits.")
        sys.exit(1)

    bit_index = 0
    new_pixels = []

    for pixel in pixels:
        r, g, b = pixel
        new_rgb = []
        for channel in (r, g, b):
            if bit_index < len(bits):
                # Replace LSB of channel with message bit
                channel = (channel & ~1) | int(bits[bit_index])
                bit_index += 1
            new_rgb.append(channel)
        new_pixels.append(tuple(new_rgb))

    img.putdata(new_pixels)
    img.save(output_path, format='PNG')
    print(f"\n[✔] Message hidden successfully!")
    print(f"[✔] Stego image saved → {output_path}")
    print(f"[i] Bits used: {bit_index} / {max_bits} ({(bit_index/max_bits)*100:.2f}% capacity used)")


def extract_lsb(image_path: str) -> bytes:
    """
    Extract hidden encrypted bytes from a stego image using LSB.
    """
    img = Image.open(image_path).convert('RGB')
    pixels = list(img.getdata())

    bits = ""
    for pixel in pixels:
        for channel in pixel:
            bits += str(channel & 1)

    # Convert bits to bytes and decode base64 payload
    raw_bytes = bits_to_bytes(bits)
    raw_str = raw_bytes.decode(errors='ignore')

    if DELIMITER not in raw_str:
        print("[!] No hidden message found or image is corrupted.")
        sys.exit(1)

    payload = raw_str.split(DELIMITER)[0]
    return base64.b64decode(payload)


# ─────────────────────────────────────────
#  MAIN FUNCTIONS
# ─────────────────────────────────────────

def encode(image_path: str, message: str, password: str, output_path: str):
    """Full pipeline: AES Encrypt → LSB Embed."""
    print("\n[*] Encrypting message with AES-256...")
    encrypted = aes_encrypt(message, password)
    print(f"[*] Encrypted size: {len(encrypted)} bytes")

    print("[*] Embedding into image using LSB...")
    embed_lsb(image_path, encrypted, output_path)


def decode(image_path: str, password: str):
    """Full pipeline: LSB Extract → AES Decrypt."""
    print("\n[*] Extracting hidden data from image...")
    encrypted_data = extract_lsb(image_path)
    print(f"[*] Extracted {len(encrypted_data)} bytes of encrypted data")

    print("[*] Decrypting with AES-256...")
    try:
        message = aes_decrypt(encrypted_data, password)
        print(f"\n[✔] Hidden Message:\n{'─'*40}\n{message}\n{'─'*40}")
    except Exception:
        print("[!] Decryption failed. Wrong password or tampered image.")
        sys.exit(1)


def check_capacity(image_path: str):
    """Check how many characters an image can hide."""
    img = Image.open(image_path).convert('RGB')
    pixels = len(list(img.getdata()))
    max_bytes = (pixels * 3) // 8
    # Subtract overhead: base64 expansion (~33%), AES padding (16), IV (16), delimiter
    usable = int(max_bytes * 0.72) - 50
    print(f"\n[i] Image     : {image_path}")
    print(f"[i] Dimensions: {img.size[0]}x{img.size[1]} px")
    print(f"[i] Max capacity: ~{usable} characters")


# ─────────────────────────────────────────
#  CLI INTERFACE
# ─────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="🔐 AES-256 + LSB Image Steganography Tool by Sanjay G",
        formatter_class=argparse.RawTextHelpFormatter
    )
    subparsers = parser.add_subparsers(dest='command')

    # Encode command
    enc = subparsers.add_parser('encode', help='Hide a secret message in an image')
    enc.add_argument('-i', '--image',   required=True, help='Input cover image path')
    enc.add_argument('-m', '--message', required=True, help='Secret message to hide')
    enc.add_argument('-p', '--password',required=True, help='AES encryption password')
    enc.add_argument('-o', '--output',  required=True, help='Output stego image path (.png)')

    # Decode command
    dec = subparsers.add_parser('decode', help='Extract a hidden message from an image')
    dec.add_argument('-i', '--image',    required=True, help='Stego image path')
    dec.add_argument('-p', '--password', required=True, help='AES decryption password')

    # Capacity command
    cap = subparsers.add_parser('capacity', help='Check how much data an image can hide')
    cap.add_argument('-i', '--image', required=True, help='Image path')

    args = parser.parse_args()

    print("""
╔══════════════════════════════════════════════╗
║   🔐 AES + LSB Steganography Tool            ║
║   By Sanjay G | github.com/sanjaybx1         ║
╚══════════════════════════════════════════════╝""")

    if args.command == 'encode':
        if not args.output.endswith('.png'):
            print("[!] Output must be a .png file to preserve LSB data.")
            sys.exit(1)
        encode(args.image, args.message, args.password, args.output)

    elif args.command == 'decode':
        decode(args.image, args.password)

    elif args.command == 'capacity':
        check_capacity(args.image)

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
