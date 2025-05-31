# 📦 Saibyo: Deep Learning Video Frame Interpolation Library

[![CI - Python UV](https://github.com/alrodsa/saibyo/actions/workflows/python-ci.yml/badge.svg)](https://github.com/alrodsa/saibyo/actions/workflows/python-ci.yml)

---

## Overview

**Saibyo** is a Python library designed to perform video frame interpolation using deep learning techniques. Its primary goal is to enhance the fluidity of videos by generating intermediate frames between existing ones. This is especially useful for applications like:

- 🖼️ Smoothing low-FPS footage
- 🎞️ Creating slow-motion effects
- 🧪 Preprocessing datasets for computer vision tasks

### 🚀 What Saibyo Does

- Takes a sequence of video frames as input.
- Uses a configurable number of intermediate frames per pair, controlled by the `exp` parameter (e.g., `exp=2` → 3 new frames per pair).
- Outputs an enriched sequence of frames to a specified directory.

### 🛠 Features

- ✅ Easy-to-use CLI and programmatic APIs.
- 🧬 Pydantic-based configuration system via `.conf` files or environment variables.
- ⚙️ Support for batch processing and parallel data loading via `num_workers`.

---

## ⚙️ Setting up `SaibyoConf` variables

Saibyo provides a flexible configuration system powered by **Pydantic Settings**, enabling users to configure interpolation behavior either through `.conf` files or directly via environment variables.

### 🧬 Configuration Structure in Code

The configuration model used by Saibyo is defined in [`src/saibyo/conf/conf.py`]. It follows the structure below using `pydantic-settings` to manage configuration from files or environment variables.

```python
class InterpolatorConf(BaseSettings):
    batch_size: int = Field(default=1, gt=0)
    num_workers: int = Field(default=0, ge=0)
    exp: int = Field(default=1, gt=0)

    model_config = SettingsConfigDict(env_prefix="SAIBYO_INTERPOLATOR_")
```

```python
class SaibyoConf(Conf, BaseSettings):
    interpolator: InterpolatorConf = Field(default_factory=InterpolatorConf)

    model_config = SettingsConfigDict(env_prefix="SAIBYO_")
```


### 🔧 Configuration Methods

There are **two ways** to configure Saibyo:

#### 1️⃣ Using `.conf` files

You can load configuration from predefined files located in the `conf/` directory:

```
conf/
├── development/
│   └── application.conf
└── production/
    └── application.conf
```

To select which file is used, you must set the environment variable `ENV`:

```bash
export ENV=development
# or
export ENV=production
```

This tells Saibyo to automatically read the corresponding file under `conf/{ENV}/application.conf`.

These files define the configuration block for the interpolator, such as:

```yaml
[interpolator]
batch_size = 4
num_workers = 0
exp=2
```

#### 2️⃣ Using Environment Variables

You can also configure Saibyo directly via environment variables, without relying on `.conf` files. This is ideal for containerized deployments or CI environments.

The `InterpolatorConf` uses the prefix `SAIBYO_INTERPOLATOR_`. Valid environment variables include:

| Environment Variable              | Description                                    | Default |
|----------------------------------|------------------------------------------------|---------|
| `SAIBYO_INTERPOLATOR_BATCH_SIZE` | Number of image pairs per batch                | `1`     |
| `SAIBYO_INTERPOLATOR_NUM_WORKERS`| Number of parallel PyTorch workers             | `0`     |
| `SAIBYO_INTERPOLATOR_EXP`        | Power of 2 for interpolated frame generation   | `1`     |

Set them like this:

```bash
export SAIBYO_INTERPOLATOR_BATCH_SIZE=4
export SAIBYO_INTERPOLATOR_NUM_WORKERS=2
export SAIBYO_INTERPOLATOR_EXP=3
```

> #### 🧠 Understanding `exp` (Exponent)
>
>The `exp` parameter controls how many frames are interpolated between each original pair:
>
>| `exp` | Interpolated Frames | Final Frame Count (per pair) | Multiplier |
>|-------|---------------------|-------------------------------|------------|
>| 1     | 1                   | 2                             | 2×         |
>| 2     | 3                   | 4                             | 4×         |
>| 3     | 7                   | 8                             | 8×         |
>
>This allows flexible fine-tuning between speed and quality depending on the use case.

---

## 🚀 Usage: Interpolating Video Frames

The `interpolate` functionality in Saibyo can be executed in two main ways:

### 1️⃣ Command-Line Interface (CLI)

Run the interpolation directly using the CLI:

```bash
python main.py interpolate input_folder output_folder
```

### 2️⃣ Programmatic API Usage

Invoke the interpolation in your Python code:

```python
conf = configure(APP_NAME, ROOT_DIR, SaibyoConf)
Interpolator(conf).run(
    input_folder=input_folder,
    output_folder=output_folder,
)
```

### 🖼 Input and Output Behavior

- **Input Folder:** Should contain sequential frames.
- **Output Folder:** Will be populated with the original frames plus new interpolated frames between each pair.
- **Interpolation Depth:** Controlled by the `exp` value in the configuration, which determines how many intermediate frames are generated between each input pair.

For example:
- `exp=1` → 1 interpolated frame (2x FPS)
- `exp=2` → 3 interpolated frames (4x FPS)
- `exp=3` → 7 interpolated frames (8x FPS)


