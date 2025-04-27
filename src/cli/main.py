import fire

from src.cli.interpolate import interpolate


def main() -> None:
    """
    CLI entrypoint.
    """
    fire.Fire({
        "interpolate": interpolate,
    })
