from _internal.commands.base_command import BaseCommand
from _internal.lang.parser import parse
from _internal.interpreteur.interpreteur import interpret
from _internal.lang.ast import LangAst
from pathlib import Path

class BuildCommand(BaseCommand):

    name = "build"
    help = "Build a project"
    option = []

    def main(self, *args):
        astral_file = Path() / "AstralFile"
        if astral_file.exists():
            with open(astral_file) as f:
                content = f.read()
        else:
            print("No astral file found")
            return
        
        parsed = parse(content, "_internal/lang/rule.lark")
        ast = LangAst.from_node_ast(parsed)
        interpret(ast)

