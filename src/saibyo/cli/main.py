import fire

from saibyo.cli.interpolate import interpolate


def main() -> None:
    """
    CLI entrypoint.
    """
    fire.Fire({
        "interpolate": interpolate,
    })
