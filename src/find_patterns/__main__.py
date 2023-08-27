"""CLI entrypoint for findme.

See the scripts section of the poetry documentation for more on how this entrypoint is installed via pip.
"""
import os
import sys
import argparse

from typing import List, Any
from textwrap import dedent
from enum import Enum

from rich import print as rprint
from rich.table import Table

import rich_argparse

from find_patterns.config import Pattern, load_config, save_config, get_default_config_location
from find_patterns.search import find_pattern
from find_patterns.exceptions import DuplicateAliasError


_FINDME_RICH_FORMAT = "[blue bold]findme[/]"


DESCRIPTION_STRING = f"""
[underline]{_FINDME_RICH_FORMAT}[/] manages regex patterns so you can find specific kinds of files quickly.

Use the following commands to manage patterns:

    {_FINDME_RICH_FORMAT} [bold]--add [dim]<pattern name>[/] [bold]--pattern [dim]<pattern>[/]
    {_FINDME_RICH_FORMAT} [bold]--remove [dim]<pattern name>[/]
    {_FINDME_RICH_FORMAT} [bold]--list[/]

Once you have patterns defined, call

    {_FINDME_RICH_FORMAT} [dim]<pattern>[/]

To quickly locate any matching resources on disk.
See the end of this message for additional examples.
"""

EPILOG_STRING = """
Examples:

    findme --add py --pattern "\.py$"                          Add a pattern to locate all python files on disk.
    findme --add maya --pattern "\.m\[ab]$"                     Add a pattern to locate all autodesk maya files (.ma, .mb)
    findme --add templates --pattern "\.(inl|\[ht]cc|\[ht]pp)$"  Add a pattern to locate all c++ template files
    findme --add activate --pattern "activate$" --files-only   Add a pattern to locate all files named "activate"

    findme templates ./project_dir/include                     Search for all c++ template files inside the given directory.

    findme maya | wc -l | ...                                  Search for maya files and perform other operations with the filepaths.

    findme --remove py                                         Remove the alias we previously created for python files.

    findme --list                                              List all aliases that are assigned.
"""


# TODO: Should be ported to a more streamlined library like Typer. Just want to get something initially working.
def parse_args():
    parser = argparse.ArgumentParser(
        description=DESCRIPTION_STRING,
        epilog=EPILOG_STRING,
        formatter_class=rich_argparse.RawDescriptionRichHelpFormatter,
    )

    parser.add_argument("pattern_name", nargs="?", help="Pattern(s) to search for.")

    parser.add_argument(
        "search_root",
        nargs="?",
        help="Directory to search in (defaults to current directory.)",
    )

    parser.add_argument(
        "-a",
        "--add",
        help="Alias for pattern to add. Must be used in conjunction with --pattern.",
    )
    parser.add_argument(
        "-p", "--pattern", help="Regex pattern to be added for the given alias."
    )
    parser.add_argument(
        "-f",
        "--files-only",
        action="store_true",
        help="Only match this pattern against files.",
    )
    parser.add_argument(
        "-d",
        "--directories-only",
        action="store_true",
        help="Only match this pattern against directories.",
    )

    parser.add_argument(
        "-r", "--remove", help="Remove the given alias from the config."
    )

    parser.add_argument(
        "-l", "--list", action="store_true", help="List current patterns."
    )

    parser.add_argument(
        "-c", "--config", action="store_true", help="Display location of config file."
    )

    args = parser.parse_args()

    if args.add and not args.pattern:
        parser.error("Must use --add in conjunction with --pattern.")

    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(0)

    return args


def app():
    ### Parse cli args
    args = parse_args()

    ### --list
    if args.list:
        list_patterns()

    ### --add
    if args.add:
        add_pattern(args.add, args.pattern, args.files_only, args.directories_only)

    ### --remvoe
    if args.remove:
        remove_pattern(args.remove)

    ### --config
    if args.config:
        print("Config located at", get_default_config_location())
        sys.exit(0)

    ### Search for pattern
    search_for_pattern(args.pattern_name, args.search_root)


def search_for_pattern(alias: str, search_root: str):
    """Search on disk for the given `alias`."""
    patterns = _try_load_config()

    pattern_to_search_for = next((p for p in patterns if p.alias == alias), None)

    if not pattern_to_search_for:
        _print_error(f"Pattern {alias} not found")
        sys.exit(1)

    for match in find_pattern(search_root or os.getcwd(), pattern_to_search_for):
        print(match)

    sys.exit(0)


def list_patterns():
    """List the current patterns defined in the config file."""
    patterns = _try_load_config()

    if not patterns:
        print("No patterns saved in config.")
    else:
        _print_patterns_in_table(patterns)

    sys.exit(0)


def add_pattern(alias: str, pattern: str, files_only: bool, directories_only: bool):
    """Attempt to add the given `alias` to the config file with the given parameters."""
    patterns = _try_load_config()

    new_pattern = Pattern(
        alias=alias,
        pattern=pattern,
        files_only=files_only,
        directories_only=directories_only,
    )

    patterns.append(new_pattern)

    try:
        save_config(patterns)
    except DuplicateAliasError as e:
        _print_error(str(e))
        sys.exit(1)

    print("Added the following pattern:")
    _print_patterns_in_table([new_pattern])

    sys.exit(0)


def remove_pattern(alias: str):
    """Attempt to remove the given `alias` from the config file."""
    patterns = _try_load_config()

    pattern_to_remove = next((p for p in patterns if p.alias == alias), None)

    if pattern_to_remove:
        patterns.remove(pattern_to_remove)
        save_config(patterns)
        sys.exit(0)
    else:
        _print_error(f"Pattern {alias} not found in config.")
        sys.exit(1)


def _print_patterns_in_table(patterns: List[Pattern]):
    """Print a rich table displaying the contents of `patterns`."""
    table = Table("Pattern name", "Pattern", "Files only?", "Directories only?")

    for pattern in patterns:
        table.add_row(
            pattern.alias,
            pattern.pattern,
            _color_string(pattern.files_only),
            _color_string(pattern.directories_only),
        )

    rprint(table)


def _try_load_config():
    """Try and load the config file from disk. Return no patterns if the config cannot be found."""
    try:
        return load_config()
    except FileNotFoundError:
        return []


def _color_string(m: Any) -> str:
    """Return a rich formatted string for `m`, colored green or red based on the truthiness of `m`."""
    return f"[{'green' if m else 'red'}]{str(m)}[/]"


def _print_error(message: str):
    """Format a small error string."""
    rprint(f"[bold red]ERROR: [/]{message}")


if __name__ == "__main__":
    app()
