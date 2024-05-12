from _internal.osinfo import get_cpp_default_compiler, get_c_default_compiler

class Env:
    def __init__(self) -> None:
        self.includes = []
        self.flags = []
        self.vars = {}
        self.files = []
        self.compiler = get_c_default_compiler()

