
from _internal.commands import load_command
from _internal.commands.init_command import InitCommand
from _internal.commands.parse_command import ParseCommand
from _internal.commands.build_command import BuildCommand
import click





@click.group()
def cli():
    pass


load_command(click, cli, [InitCommand, ParseCommand, BuildCommand])

if __name__ == '__main__':
    cli()