"""CLI entrypoint for findme."""
import sys
import argparse

from textwrap import dedent
from enum import Enum

from rich.markdown import Markdown

from rich_argparse import RawDescriptionRichHelpFormatter


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


def app():
    show_help = "-h" in sys.argv or "--help" in sys.argv
    no_commands = len(sys.argv) == 1
    search_for_pattern = len(sys.argv) > 1 and (sys.argv[1] not in [e.value for e in Commands])

    if show_help and search_for_pattern:
        sys.argv = [sys.argv[0], "--help"]

    add_subparsers = show_help or no_commands or not search_for_pattern

    print("Search for pattern?", search_for_pattern)
    print("add subparsers?", add_subparsers)

    ### Parse command line args 
    parser = argparse.ArgumentParser(description=DESCRIPTION_STRING, formatter_class=RawDescriptionRichHelpFormatter)

    if not add_subparsers:
        parser.add_argument("pattern", nargs='?')
    
    else:
        command_subparser = parser.add_subparsers(dest="command")

        # Parser for add command
        add_parser = command_subparser.add_parser("add", help="Add a pattern.", formatter_class=RawDescriptionRichHelpFormatter)
        add_parser.add_argument("pattern", help="Name of the pattern to add.")
        add_parser.add_argument("regex", help="Regex for this pattern.")
        add_parser.add_argument("-o", "--overwrite", action="store_true", help="Overwrite the pattern if it already exists.")

        # Parser for remove command
        remove_parser = command_subparser.add_parser("remove", help="Remove a pattern.", formatter_class=RawDescriptionRichHelpFormatter)
        remove_parser.add_argument("pattern", help="Name of the pattern to remove.")
        
        # Parser for list command
        list_parser = command_subparser.add_parser("list", help="List patterns.", formatter_class=RawDescriptionRichHelpFormatter)

    parser.parse_args()

    # Exit with help message if no args supplied
    if len(sys.argv) == 1:
        parser.print_help(sys.stderr)
        sys.exit(0)

    # Determine whether the supplied arg is a valid command, or a user defined alias
    command = sys.argv[1]

    print(parser.parse_args())


if __name__ == "__main__":
    app()
