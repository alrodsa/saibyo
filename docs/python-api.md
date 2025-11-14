# 🐍 Saibyo Python API Guide

Saibyo provides a simple Python API that allows you to:

- Interpolate a video using deep learning
- Generate comparison videos
- Customize behavior through `SaibyoConf`

This guide covers the **public-facing API** for programmatic use.


## ⚙️ Loading Configuration

Saibyo uses `SaibyoConf` to manage all settings for interpolation and comparison.

Load the full configuration like this:

```python
from saibyo.conf.conf import SaibyoConf
from saibyo.base.conf.app import configure
from saibyo.constants.app import APP_NAME, ROOT_DIR

conf = configure(APP_NAME, ROOT_DIR, SaibyoConf)
```

This automatically loads:

- default settings
- environment variables (`SAIBYO_*`)
- nested configuration blocks (`InterpolatorConf`, `ComparatorConf`)

👉 Full configuration options are documented here:
**[`docs/configuration.md`](configuration.md)**

---

## 🎥 Interpolating Videos (Python API)

Interpolation is done through the `Interpolator` class, which automatically uses the configuration loaded above.

### Example

```python
from saibyo.conf.conf import SaibyoConf
from saibyo.base.conf.app import configure
from saibyo.core.interpolation.interpolator import RifeInterpolator
from saibyo.constants.app import APP_NAME, ROOT_DIR

# Load configuration
conf = configure(APP_NAME, ROOT_DIR, SaibyoConf)

# Create interpolator
interpolator = RifeInterpolator(conf)

# Run interpolation
interpolator.run(
    input_path="input.mp4",
    output_folder="output/"
)
```

### Behavior

- Uses the **RIFE** model for deep-learning interpolation
- The output FPS multiplier is determined by:

```python
multiplier = 2 ** conf.interpolator.exponential
```

- FP16 mode can be enabled via `conf.interpolator.lightweight`
- If `conf.interpolator.comparation=True`, a comparison video is also generated

> **Reference:** Refer to the full details about configuration options and behavior in [`docs/configuration.md`](configuration.md)


## 🎛 Comparing Videos (Python API)

Comparison is performed by the `Comparator` class:

```python
from saibyo.conf.conf import SaibyoConf
from saibyo.base.conf.app import configure
from saibyo.core.comparation.comparator import Comparator
from saibyo.constants.app import APP_NAME, ROOT_DIR

# Load configuration
conf = configure(APP_NAME, ROOT_DIR, SaibyoConf)

# Create comparator
comparator = Comparator(conf.comparator)

# Run comparison
comparator.compare(
    video_a="original.mp4",
    video_b="interpolated.mp4",
    output_path="comparison.mp4"
)
```

### Behavior

- Places both videos in a composite canvas
- Layout depends on:


> **Reference:** Refer to the full details about comparison modes and configuration options in [`docs/comparison-modes.md`](comparison-modes.md)
