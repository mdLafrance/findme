"""CLI entrypoint for findme."""
import os
import sys
import argparse

from typing import List, Any
from textwrap import dedent
from enum import Enum

from rich import print as rprint
from rich.table import Table

from findme.config import Pattern, load_config, save_config
from findme.search import find_pattern
from findme.exceptions import DuplicateAliasError


DESCRIPTION_STRING = """
findme helps you find files quickly

Manage regex patterns to look for specific kinds of files.

Use the following commands to manage patterns:

    [bold]--add [dim]<pattern name> <pattern>[/]
    [bold]--remove [dim]<pattern name>[/]
    [bold]--list[/]

Call [dim]--help[/] with any of these commands to see additional help information for each.
    
    [bold]findme [dim]<command> --help[/] 


Once you have patterns defined, call

    [bold]findme [dim]<pattern>[/]

To quickly locate any matching resources on disk.
"""


class Commands(str, Enum):
    """List of expected cli commands."""

    ADD = "add"
    REMOVE = "remove"
    LIST = "list"
    CONFIG = "config"


def parse_args():
    parser = argparse.ArgumentParser()

    parser.add_argument("pattern_name", nargs="?", help="Pattern(s) to search for.")

    parser.add_argument("search_root", nargs="?", help="Directory to search in (defaults to current directory.)")

    parser.add_argument("-a", "--add", help="Alias for pattern to add. Must be used in conjunction with --pattern.")
    parser.add_argument("-p", "--pattern", help="Regex pattern to be added for the given alias.")
    parser.add_argument("-f", "--files-only", action="store_true", help="Only match this pattern against files.")
    parser.add_argument("-d", "--directories-only", action="store_true", help="Only match this pattern against directories.")

    parser.add_argument("-r", "--remove", help="Remove the given alias from the config.")

    parser.add_argument("-l", "--list", action="store_true", help="List current patterns.")

    args = parser.parse_args()

    if args.add and not args.pattern:
            parser.error("Must use --add in conjunction with --pattern.")

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

    ### Search for pattern
    search_for_pattern(args.pattern_name, args.search_root)


def search_for_pattern(alias: str, search_root: str):
    patterns = _try_load_config()

    pattern_to_search_for = next((p for p in patterns if p.alias == alias), None)

    if not pattern_to_search_for:
        _print_error(f"Pattern {alias} not found")
        sys.exit(1)

    for match in find_pattern(search_root or os.getcwd(), pattern_to_search_for):
        print(match)

    sys.exit(0)


def list_patterns():
    patterns = _try_load_config()

    if not patterns:
        print("No patterns saved in config.")
    else:
        _print_patterns_in_table(patterns)

    sys.exit(0)


def add_pattern(alias: str, pattern: str, files_only: bool, directories_only: bool):
    patterns = _try_load_config()

    new_pattern = Pattern(alias=alias, pattern=pattern, files_only=files_only, directories_only=directories_only)

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
    table = Table("Pattern name", "Pattern", "Files only?", "Directories only?")

    for pattern in patterns:
        table.add_row(pattern.alias, pattern.pattern, _color_string(pattern.files_only), _color_string(pattern.directories_only))

    rprint(table)


def _try_load_config():
    try:
        return load_config()
    except FileNotFoundError:
        return []


def _color_string(m: Any) -> str:
    return f"[{'green' if m else 'red'}]{str(m)}[/]"


def _print_error(message: str):
    rprint(f"[bold red]ERROR: [/]{message}")
     


if __name__ == "__main__":
    app()
