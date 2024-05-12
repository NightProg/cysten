

class LangBuilder:
    def __init__(self):
        self.lang = ""

    def add_line(self, line):
        self.lang += line + "\n"

    def add_tab(self, line):
        self.lang += "\t" + line + "\n"

    def package(self, name, description=None, author=None, license=None, version=None):
        self.add_line("package %s {" % name)

        if description:
            self.add_tab(f"description {description}")

        if author:
            self.add_tab(f"author {author}")

        if license:
            self.add_tab(f"license {license}")

        if version:
            self.add_tab(f"version {version}")

        self.add_line("}")
    
    def require(self, name, version=None):
        self.add_line("require %s {" % name)

        if version:
            self.add_tab(f"version {version}")
        
        self.add_line("}")
    
    def build(self):
        return self.lang
    
    def write(self, path):
        with open(path, "w") as f:
            f.write(self.build())


