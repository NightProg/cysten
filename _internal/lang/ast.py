from typing import NamedTuple
from _internal.lang.builder import LangBuilder
from _internal.util.option import Option
from _internal.util.version import Version
from _internal.util.license import License

from lark.tree import Tree

def string(s):
    return s[1:-1]

class Exe(NamedTuple):
    name: str
    files: list[str]
    links: list[str]
    alls: list[str]

    def from_node_ast(tree: Tree):
        if tree.data != "exe":
            raise Exception("Invalid exe node")
        files = []
        links = []
        alls = []
        name = string(tree.children[0].value)
        for node in tree.children[1:]:
            node = node.children[0]
            if node.data == "exe_file":
                files.append(
                    string(node.children[0].value)
                    )
            elif node.data == "exe_link":
                links.append(
                    string(node.children[0].value)
                    )
            elif node.data == "exe_all":
                alls.append(
                    string(node.children[0].value)
                )
            else:
                raise Exception(f"Invalid node: {node.data}")
        return Exe(name, files, links, alls)
    
    def __str__(self) -> str:
        return "exe %s {\n\t%s\n\t%s\n\t%s\n}" % (
            self.name,
            "\n".join(map(lambda x: f"file {x}", self.files)),
            "\n".join(map(lambda x: f"all {x}", self.alls)),
            "\n".join(map(lambda x: f"link {x}", self.links))
        ) 

class Include(NamedTuple):
    path: str

    def from_node_ast(tree: Tree):
        if tree.data != "include":
            raise Exception("Invalid include node")
        return Include(string(tree.children[0].value))
    
    def __str__(self):
        return f"include {self.path}"

    def to_builder(self, builder: LangBuilder):
        builder.add_line(f"include {self.path}")

class IncludeAll(NamedTuple):
    path: str

    def from_node_ast(tree: Tree):
        if tree.data != "include_all":
            raise Exception("Invalid include_all node")
        return IncludeAll(tree.children[0].value)
    
    def __str__(self):
        return f"include_all {self.path}"

    def to_builder(self, builder: LangBuilder):
        builder.add_line(f"include_all {self.path}")

class Require(NamedTuple):
    path: Option
    version: Option
    name: str

    def from_node_ast(tree: Tree):
        if tree.data != "require":
            raise Exception("Invalid require node")
        name = tree.children[0].value
        path = None
        version = None
        children = tree.children[2]
        for node in tree.children[1:]:
            node = node.children[0]
            if node.data == "require_from":
                path = node.children[0].value
            elif node.data == "require_version":
                children = node.children[0].children 
                if len(children) == 1:
                    version = Version(int(children[0].value), 0, 0)
                elif len(children) == 2:
                    version = Version(int(children[0].value), int(children[1].value), 0)
                elif len(children) == 3:
                    version = Version(int(children[0].value), int(children[1].value), int(children[2].value))
            else:
                raise Exception(f"Invalid node: {node.data}")

        return Require(Option(path), Option(version), name)
    
    def to_builder(self, builder: LangBuilder):
        builder.require(self.name, version=self.version)

    def __str__(self):
        return f"require {self.name} {{\n" + \
            (f"\tpath {self.path}\n" if self.path else "") + \
            (f"\tversion {self.version}\n" if self.version else "") + \
            "}"


class Package(NamedTuple):
    name: str
    description: Option
    version: Option
    author: Option
    license: Option

    def from_node_ast(tree: Tree):
        if tree.data != "package":
            raise Exception("Invalid package node")
        name = tree.children[0].value
        pkg_meta = tree.children[1]

        if pkg_meta.data != "package_meta":
            raise Exception("Invalid package meta node")
        
        description = None
        version = None
        author = None
        license = None
        if len(pkg_meta.children) > 0:
            for meta in pkg_meta.children:
                if meta.data == "description_id":
                    description = meta.children[0].value
                elif meta.data == "version_id":
                    version = Version.from_string(meta.children[0].value)
                elif meta.data == "author_id":
                    author = meta.children[0].value
                elif meta.data == "license_id":
                    license = License.from_string(meta.children[0].value)

        return Package(name, Option(description), Option(version), Option(author), Option(license))

                


    def __str__(self):
        return f"package {self.name} {{\n" + \
            (f"\tdescription {self.description}\n" if self.description else "") + \
            (f"\tversion {self.version}\n" if self.version else "") + \
            (f"\tauthor {self.author}\n" if self.author else "") + \
            (f"\tlicense {self.license}\n" if self.license else "") + \
            "}"
    
    def to_builder(self, builder: LangBuilder):
        builder.package(self.name, description=self.description, version=self.version, author=self.author, license=self.license)

    

class LangAst(NamedTuple):
    requires: list[Require]
    package: Package
    includes: list[Include]
    includes_all: list[IncludeAll]
    exes: list[Exe]

    def from_node_ast(tree: Tree):
        if tree.data != "start":
            raise Exception("Invalid lang node")
        requires = []
        includes = []
        includes_all = []
        exes = []
        package = None
        for children in tree.children:
            for node in children.children:
                if node.data == "require":
                    requires.append(Require.from_node_ast(node))
                elif node.data == "package":
                    package = Package.from_node_ast(node)
                elif node.data == "include":
                    include = Include.from_node_ast(node)
                    includes.append(include)
                elif node.data == "include_all":
                    include_all = IncludeAll.from_node_ast(node)
                    includes_all.append(include_all)
                elif node.data == "exe":
                    exe = Exe.from_node_ast(node)
                    exes.append(exe)
                else:
                    raise Exception(f"Invalid node: {node.data}")
        
        return LangAst(requires, package, includes, includes_all, exes)
    
    def to_builder(self, builder: LangBuilder):
        for require in self.requires:
            require.to_builder(builder)
        self.package.to_builder(builder)

    def __str__(self):
        return "\n".join(map(str, self.requires)) + \
                "\n" + str(self.package) + "\n" + \
                "\n".join(map(str, self.includes)) + \
                "\n" + "\n".join(map(str, self.includes_all)) + "\n" + \
                "\n".join(map(str, self.exes))
    
    def write(self, path):
        builder = LangBuilder()
        self.to_builder(builder)
        builder.write(path)

