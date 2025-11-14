# 🎨 Comparison Modes — Saibyo

Saibyo includes a flexible video comparison engine designed to help analyze differences between two videos side-by-side, stacked, or split visually.
The comparison output is controlled by `ComparatorConf` and rendered by the `ComparationEngine`.

## 🧩 How Comparison Works

When comparing two videos, Saibyo:

1. Loads configuration from `SaibyoConf.comparator`
2. Builds a **canvas** sized to fit both videos according to the mode
3. Reads synchronized frames from both videos
4. Composes them onto the canvas
5. Adds optional overlay text
6. Writes the composite frames to the output video

## Run Comparison

Once configured all configuration variables from `ComparatorConf`, there are two ways to run the comparison:

1. **Command Line Interface**:

```bash
saibyo compare path/to/video_a.mp4 path/to/video_b.mp4 path/to/output_comparison.mp4
```

2. **Python API**:

```python
from saibyo.conf.conf import SaibyoConf
from saibyo.comparator.comparator import Comparator

conf = SaibyoConf()
video_a = "path/to/video_a.mp4"
video_b = "path/to/video_b.mp4"
output_path = "path/to/output_comparison.mp4"

Comparator(conf.comparator).compare(video_a, video_b, output_path)
```

This uses:

- `ComparationEngine` → performs frame‑by‑frame composition
- `Canvas` → creates and assembles comparison layouts
- `OverlayTextConf` → controls overlay text and positioning

## 🎛 Available Comparison Modes

Saibyo supports four comparison modes. There are controlled by the `mode` field in `ComparatorConf`. There are two ways to set the mode:

1. **Environment Variable**: Through the exportation of the following variable:

```bash
export SAIBYO_COMPARATOR_MODE=side_by_side
```

2. **Python Configuration**: Creating or modifying the ComparatorConf instance directly and then asigning it to the SaibyoConf instance:

```python
from saibyo.conf.conf import SaibyoConf, ComparatorConf

conf = SaibyoConf(
    comparator=ComparatorConf(
        mode="side_by_side"
    )
)
```

The available modes are set inside the `ModeType` located in `saibyo.constants.conf` as follows:

```python
ModeType = Literal[
    "side_by_side",
    "top_bottom",
    "split_half_vertical",
    "split_half_horizontal"
]
```

### 🟥 1. `side_by_side`

Two full videos placed horizontally next to each other. As shown below:

![side_by_side](https://media3.giphy.com/media/v1.Y2lkPTc5MGI3NjExaGI4Y2QzaHJhNXV1NmMwY254YTJ4dG5laTIwd3JkZDJ1aTJwaWx3eiZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/WeKp0kIX9PrvhiCUDh/giphy.gif)

### Best for:
- Direct visual comparison
- Horizontal footage

### 🟧 2. `top_bottom`

Two full videos stacked vertically.

![top_bottom](https://media4.giphy.com/media/v1.Y2lkPTc5MGI3NjExOXVsOTA5NHFiOG5kb29hMGE4bHZ5NXM0N2dteGY1eTR4bHJleGkxMiZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/IjudFqP0BsL5nbX3Ep/giphy.gif)

Best for mobile screens or long‑aspect content.

### 🟨 3. `split_half_vertical`
A single composite frame where the **left half** is Video A and the **right half** is Video B.

![split_half_vertical](https://media3.giphy.com/media/v1.Y2lkPTc5MGI3NjExbWt4Z2lwbTI1ZWc1OGsyYzc4NWxqbnZiZWxoM2h1NTlzaWUzemtucCZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/NDxKHa0IJ8pJNm4DW1/giphy.gif)


### 🟦 4. `split_half_horizontal`

A single composite frame where the **top** is Video A and the **bottom** is Video B.

![split_half_horizontal](https://media3.giphy.com/media/v1.Y2lkPTc5MGI3NjExd3pkem5qN2dhYzA0czN5NDM2dnZhcnY5azZnaWQ2eXoyOWhham0yZyZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/PKI2iwYPO2FJNVEx9D/giphy.gif)

Best for progressive motion comparisons.

## 📝 Overlay Text

Overlay text can be set to identify each video source. There are two ways to enable overlay text:

1. **Environment Variable**: Through the exportation of the following variable:

```bash
export SAIBYO_COMPARATOR_OVERLAY_TEXT_OVERLAY=True
```

2. **Python Configuration**: Creating or modifying the OverlayTextConf instance directly and then asigning it to the ComparatorConf instance:

```python
from saibyo.conf.conf import SaibyoConf, ComparatorConf, OverlayTextConf

conf = SaibyoConf(
    comparator=ComparatorConf(
        text=OverlayTextConf(
            overlay=True,
            position="bottom_right"
        )
    )
)
```

The possible positions are set inside the TextPositionType` located in `saibyo.constants.conf` as follows:

```python
TextPositionType = Literal[
    "top_left", "bottom_left", "top_right", "bottom_right"
]
```
