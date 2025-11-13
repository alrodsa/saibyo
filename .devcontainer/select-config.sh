#!/usr/bin/env bash
set -e

echo "🔍 Checking GPU availability on host..."

HAS_GPU=false
HAS_RUNTIME=false

# Detect NVIDIA GPU (physical hardware)
if command -v nvidia-smi >/dev/null 2>&1; then
    HAS_GPU=true
fi

# Detect Docker NVIDIA runtime
if docker info 2>/dev/null | grep -qi "nvidia"; then
    HAS_RUNTIME=true
fi

if [ "$HAS_GPU" = true ] && [ "$HAS_RUNTIME" = true ]; then
    echo "✔ GPU detected — enabling GPU DevContainer"
    cp .devcontainer/devcontainer.gpu.json .devcontainer/devcontainer.override.json
else
    echo "✖ No GPU found — using CPU DevContainer"
    cp .devcontainer/devcontainer.cpu.json .devcontainer/devcontainer.override.json
fi

exit 0
