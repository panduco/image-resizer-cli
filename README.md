# 🖼️ Bulk Image Resizer CLI

A high-performance command-line tool to resize, scale, and convert hundreds of images in seconds. 
Uses multithreading to maximize CPU usage and features a real-time progress bar.

![Python](https://img.shields.io/badge/Python-3.6%2B-blue) ![License](https://img.shields.io/badge/License-MIT-yellow)

## ✨ Features

- **Bulk Processing:** Handles thousands of images in one go.
- **Multithreaded:** Utilizes all CPU cores for maximum speed.
- **Flexible Resizing:** Set specific width/height or use percentage scaling.
- **Format Conversion:** Convert between JPG, PNG, WEBP, etc.
- **Progress Bar:** Visual feedback using `tqdm`.

## 🛠️ Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/YOUR_USERNAME/image-resizer-cli.git
   cd image-resizer-cli
   ```

2. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

## 💻 Usage

```bash
python resizer.py <input_folder> <output_folder> [options]
```

### Options

| Flag | Description |
|------|-------------|
| `-w` or `--width` | Target width in pixels (maintains aspect ratio if height is empty). |
| `-H` or `--height` | Target height in pixels. |
| `-s` or `--scale` | Scale factor (e.g., `0.5` for 50%). |
| `-f` or `--format` | Output format (`JPG`, `PNG`, `WEBP`). |

### Examples

**Resize all images to width 800px:**
```bash
python resizer.py ./input ./output -w 800
```

**Scale images to 50% size:**
```bash
python resizer.py ./input ./output -s 0.5
```

**Convert all images to JPG:**
```bash
python resizer.py ./input ./output -f JPG
```

**Resize to 300x300 and convert to PNG:**
```bash
python resizer.py ./input ./output -w 300 -H 300 -f PNG
```

## 📜 License

This project is licensed under the MIT License.