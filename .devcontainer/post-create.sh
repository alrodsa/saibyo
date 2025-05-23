pdm venv create 3.10

uv sync --all-extras --all-groups

source .venv/bin/activate

python -m ensurepip --upgrade
