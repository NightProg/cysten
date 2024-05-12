import lark


def parse(s, rule):
    with open(rule) as f:
        grammar = f.read()
    parser = lark.Lark(grammar, start="start", parser="lalr")

    return parser.parse(s)

