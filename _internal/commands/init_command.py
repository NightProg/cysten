from _internal.commands.base_command import BaseCommand
import _internal.lang.builder as builder

class InitCommand(BaseCommand):

    name = "init"
    help = "Initialize a new project"
    option = [
        {
            "name": ("-n", "--name"),
            "option": {
                "help": "Project name",
                "prompt": "Project name"
            }
        },
        {
            "name": ("-d", "--description"),
            "option": {
                "help": "Project description",
                "prompt": "Description: "
            }
        },
        {
            "name": ("-a", "--author"),
            "option": {
                "help": "Project author",
                "prompt": "Author: "
            }
        },
        {
            "name": ("-v", "--version"),
            "option": {
                "help": "Project version"
            },
            "default": "0.0.1"
        }
    ]

    def main(self, *args):
        lang_builder = builder.LangBuilder()
        lang_builder.package(self.name, author=self.author, version=self.version)

