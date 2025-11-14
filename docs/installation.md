# 📥 Installation Guide — Saibyo

> Saibyo is distributed through **PyPI** and works on **Python 3.10+** with support for **CPU** and **GPU (CUDA)** execution.

## 🔧 Requirements

### **Python**
- Python **3.10+** (recommended: 3.10 or 3.11)
- Linux / macOS / Windows supported

### **System Dependencies**
Saibyo depends on:

- **FFmpeg** (recommended)
- **AV library backend**
- **PyTorch** (CPU or GPU version)

Check if FFmpeg is installed:

```bash
ffmpeg -version
```

If not, install:

- Ubuntu/Debian: `sudo apt install ffmpeg`
- macOS (Homebrew): `brew install ffmpeg`
- [Windows](https://ffmpeg.org/download.html)

## 📦 Installing Saibyo

### PyPI

To install Saibyo in the most straightforward way, use `pip` command:

```bash
pip install saibyo
```

### Github Release

Alternatively, you can download the latest release from the [GitHub Releases page](https://github.com/alrodsa/saibyo/releases).
Download the `.whl` file for your system and install it using `pip`:

```bash
pip install path/to/saibyo-x.y.z-py3-none-any.whl
```

### Installing from source (developers)

```bash
git clone https://github.com/alrodsa/saibyo.git
cd saibyo
uv sync
```

Or:

```bash
pip install -e .
```

## 🧪 Testing your installation

Once installed, you can verify the installation by running the following command:

```bash
python -c "import saibyo; print(saibyo.__version__)"
```

This should print the installed version of Saibyo without any errors.
