# 🔐 AES-256 + LSB Image Steganography

> **Hide encrypted secret messages inside images — invisible to the naked eye, unreadable without the key.**

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Cryptography](https://img.shields.io/badge/AES--256-Encryption-red?style=for-the-badge)
![OpenCV](https://img.shields.io/badge/Pillow-Image_Processing-yellow?style=for-the-badge)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)

---

## 📌 About the Project

This project combines **AES-256 encryption** with **LSB (Least Significant Bit) steganography** to securely hide secret messages inside image files. The hidden message is:

1. 🔒 **Encrypted** using AES-256 with a user-defined password
2. 🖼️ **Embedded** into the pixel data of an image (invisible to the human eye)
3. 🔓 **Extractable** only with the correct password

Even if someone finds the stego image, they cannot read the message without the password.

---

## 🧠 How It Works

```
📝 Secret Message
        ↓
🔐 AES-256 Encryption (CBC Mode + SHA-256 key derivation)
        ↓
📦 Base64 Encoding + Delimiter tagging
        ↓
🖼️ LSB Embedding into image pixels (R, G, B channels)
        ↓
💾 Stego Image saved as PNG (lossless)

━━━━━━━━━━━━ REVERSE PROCESS ━━━━━━━━━━━━

🖼️ Stego Image
        ↓
🔍 LSB Extraction from pixel channels
        ↓
📦 Base64 Decoding
        ↓
🔓 AES-256 Decryption (with correct password)
        ↓
📝 Original Secret Message
```

---

## 🛡️ Security Architecture

| Layer | Method | Details |
|---|---|---|
| 🔑 Key Derivation | SHA-256 | Password → 256-bit key |
| 🔒 Encryption | AES-256 CBC | Industry-standard encryption |
| 🎲 IV Generation | Random 16 bytes | Unique per encryption |
| 📦 Encoding | Base64 | Binary-safe payload encoding |
| 🖼️ Hiding | LSB Steganography | 1 bit per RGB channel |
| 🔚 Delimiter | `$$END$$` | Marks end of hidden payload |

---

## ✨ Features

- 🔐 **AES-256 CBC encryption** — military-grade security
- 🖼️ **LSB steganography** — visually undetectable changes
- 🖥️ **CLI Tool** — for terminal/scripting use
- 🎨 **GUI App** — user-friendly Tkinter interface
- 📊 **Capacity checker** — know how much data an image can hold
- 🛡️ **Wrong password detection** — secure decryption validation
- 💾 **PNG output** — lossless format preserves hidden bits

---

## 📁 Project Structure

```
image-steganography/
│
├── stego.py            # Core engine (AES + LSB logic)
├── gui.py              # Tkinter GUI application
├── requirements.txt    # Python dependencies
└── README.md
```

---

## ⚙️ Installation

### 1. Clone the Repository
```bash
git clone https://github.com/sanjaybx1/image-steganography
cd image-steganography
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

---

## 🚀 Usage

### 🖥️ CLI Mode

**Encode (Hide a message):**
```bash
python stego.py encode -i cover.png -m "This is my secret message" -p mypassword123 -o stego_output.png
```

**Decode (Extract the message):**
```bash
python stego.py decode -i stego_output.png -p mypassword123
```

**Check image capacity:**
```bash
python stego.py capacity -i cover.png
```

### 🎨 GUI Mode

```bash
python gui.py
```

---

## 🖼️ CLI Output Example

```
╔══════════════════════════════════════════════╗
║   🔐 AES + LSB Steganography Tool            ║
║   By Sanjay G | github.com/sanjaybx1         ║
╚══════════════════════════════════════════════╝

[*] Encrypting message with AES-256...
[*] Encrypted size: 48 bytes
[*] Embedding into image using LSB...

[✔] Message hidden successfully!
[✔] Stego image saved → stego_output.png
[i] Bits used: 3456 / 2073600 (0.17% capacity used)
```

---

## 📊 Capacity Reference

| Image Size | Max Characters (approx) |
|---|---|
| 100 × 100 px | ~2,600 chars |
| 500 × 500 px | ~65,000 chars |
| 1280 × 720 px | ~213,000 chars |
| 1920 × 1080 px | ~480,000 chars |

> ⚠️ Always use **PNG format** for output — JPEG compression destroys LSB data.

---

## ⚠️ Important Notes

- Output image **must be `.png`** — JPEG/JPG will corrupt the hidden data
- The **cover image and stego image look identical** visually
- Without the **correct password**, decryption is impossible
- Larger images = more capacity for hidden data

---

## 🚀 Future Improvements

- [ ] Support for hiding files (PDF, TXT) inside images
- [ ] Add steganography detection resistance (randomized LSB positions)
- [ ] Web app version using Flask
- [ ] Support for video steganography
- [ ] Add integrity check using HMAC

---

## 👨‍💻 Author

**Sanjay G**
- 📧 [sanjaycharles23@gmail.com](mailto:sanjaycharles23@gmail.com)
- 🐙 [github.com/sanjaybx1](https://github.com/sanjaybx1)
- 🎓 MSc Cyber Forensics & Information Security — MGR University

---

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

---

<div align="center">

*"Security through obscurity + encryption — the best of both worlds."* 🔐

⭐ **Star this repo if you found it useful!**

</div>
