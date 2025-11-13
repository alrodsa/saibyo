FROM pytorch/pytorch:2.3.0-cuda12.1-cudnn8-runtime

ENV DEBIAN_FRONTEND=noninteractive

# Instala dependencias del sistema
RUN apt update -y && apt install -y \
    git \
    python3-pip \
    zsh \
    wget \
    curl \
    unzip \
    ffmpeg \
    libsm6 \
    libxext6 \
    libimage-exiftool-perl \
    libvulkan1 \
    vulkan-tools \
    libvulkan-dev \
    libx264-dev \
    libx265-dev \
    libfdk-aac-dev \
    libmp3lame-dev \
    yasm \
    build-essential \
    libopenh264-dev \
    python3-tk \
    sudo \
    ca-certificates \
    lsb-release \
    software-properties-common \
    && rm -rf /var/lib/apt/lists/*

# Crea usuario no root
ARG USERNAME=saibyo
ARG USER_UID=1000
ARG USER_GID=$USER_UID
ARG RENDER_GID=110

RUN groupadd --gid $USER_GID $USERNAME \
    && useradd --uid $USER_UID --gid $USER_GID -m $USERNAME \
    && echo "$USERNAME ALL=(ALL) NOPASSWD:ALL" > /etc/sudoers.d/$USERNAME \
    && chmod 0440 /etc/sudoers.d/$USERNAME \
    && getent group render || groupadd -g $RENDER_GID render \
    && usermod -aG render $USERNAME

USER $USERNAME

# Instala uv y otras herramientas
RUN pip install --user uv

# Instala zsh personalizado
RUN sh -c "$(wget -O- https://github.com/deluan/zsh-in-docker/releases/download/v1.1.5/zsh-in-docker.sh)" -- -t robbyrussell
