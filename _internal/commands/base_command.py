import abc


def yad(decorators):
    def decorator(f):
        for d in reversed(decorators):
            f = d(f)
        return f

    return decorator


class BaseCommand:
    option = []
    arguments = []

    def __init__(self, click_mod, group):
        self.group = group
        self.click = click_mod

    @abc.abstractmethod
    def main(self, *args):
        pass

    def build(self):
        option = []
        argument = []
        for i in self.option:
            option.append(self.click.option(*i["name"], **i["option"]))

        for c in self.arguments:
            argument.append(self.click.argument(c["name"], **c["option"]))

        @self.click.command(self.name, help=self.help)
        @yad(option)
        @yad(argument)
        def main(*args, **kwargs):
            for i in kwargs:
                setattr(self, i, kwargs[i])
            self.main(*args)

        self.group.add_command(main)
        return main