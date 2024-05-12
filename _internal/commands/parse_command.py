from _internal.commands.base_command import BaseCommand
from _internal.lang.parser import parse
from _internal.lang.ast import LangAst

class ParseCommand(BaseCommand):
    
    name = "parse"
    help = "Parse a file"
    option = [
        {
            "name": ("-f", "--file"),
            "option": {
                "help": "File to parse",
                "prompt": "File to parse"
            }
        }
    ]

    def main(self, *args):
        with open(self.file) as f:
            content = f.read()
        
        ast = parse(content, "_internal/lang/rule.lark")
        ast = LangAst.from_node_ast(ast)
        print(ast)


