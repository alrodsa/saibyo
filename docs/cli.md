# 🎮 Saibyo CLI Guide

Saibyo provides a simple and powerful **command‑line interface** for video interpolation and comparison.
All commands are powered by the internal Python API and use your project configuration automatically.

> Before using the CLI, ensure that Saibyo is installed. Refer to the [Installation Guide](installation.md) for detailed instructions.

## 🚀 CLI Commands Overview

Saibyo exposes two main commands:

- `saibyo interpolate` → Boost video FPS.
- `saibyo compare` → Generate comparison videos between two clips.

Both commands are dispatched using **Python Fire**.

## ⚡ Command: `interpolate`

Interpolates a video using the **RIFE deep learning model**, applying the configuration defined by default in `SaibyoConf` (check [`configuration.md`](configuration.md) for more detailed information).

### **Usage**

To interpolate a video, run the following command:

```bash
saibyo interpolate <input_path> <output_folder>
```

| Argument | Type | Description |
|---------|------|-------------|
| `input_path` | str | Path to the input video to be interpolated |
| `output_folder` | str | Folder where the interpolated frames/video will be saved |

> By default, the name of the output file will be
```{original_video_name}_x{fps_multiplier}_{new_fps}.mp4```, where `fps_multiplier` is the factor by which the original FPS is increased.

## 🎨 Command: `compare`

Creates a **side‑by‑side comparison video** (or other modes depending on your configuration). It uses the `Comparator` class internally, applying the comparison mode defined by default in `SaibyoConf` (check [`comparison-modes.md`](comparison-modes.md) for more detailed information).

### **Usage**

To compare two videos, run the following command:

```bash
saibyo compare <video_a> <video_b> <output_path>
```

| Argument | Type | Description |
|---------|------|-------------|
| `video_a` | str | First video for comparison |
| `video_b` | str | Second video for comparison |
| `output_path` | str | Where the comparison video will be written |
