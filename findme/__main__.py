import typer
import argparse

from enum import Enum


class Commands(str, Enum):
    """List of expected cli commands."""

    ADD = "add"
    REMOVE = "remove"
    LIST = "list"
    WHERE = "where"

    def __contains__(self, __key: str) -> bool:
        return __key in self.__members__.values()


def parse_args():
    parser = argparse.ArgumentParser()

    


if __name__ == "__main__":
    app()
