from _internal.lang.ast import LangAst, Exe, Include, IncludeAll
from _internal.interpreteur.env import Env
from _internal.interpreteur.cc import CC
from _internal.exception.os import DirectoryNotFound, IsNotADirectory
from _internal.logs import *
from pathlib import Path
from os import listdir
from tempfile import TemporaryFile


def interpret(ast: LangAst):
    env = Env()

    for include_all in ast.includes_all:
        execute_include_all(include_all)

    for include in ast.includes:
        execute_include(include)

    for require in ast.requires:
        execute_require(env, require)

    for exe in ast.exes:
        execute_exe(env, exe)

def execute_exe(env: Env, exe: Exe):
    files = []
    for all in exe.alls:
        path = Path(all)
        if not path.is_dir():
            raise IsNotADirectory(f"{path} is not a directory")
        
        if not path.exists():
            raise DirectoryNotFound(f"{path} not found")
        
        files.extend(listdir(str(path)))
    
    for file in exe.files:
        files.append(file)

    cc = CC(env.compiler)
    cc.files = files
    cc.includes = env.includes
    cc.flags = env.flags
    cc.output = exe.name

    info(f"Compiling {exe.name}")
    info(f"Running {cc}")

    res = cc.execute()

    if res.returncode != 0:
        error(f"Failed to compile {exe.name}")
        error(f"Error code: {res.returncode}")
        error(f"Error message: {res.stderr}")
        return
    
    success(f"Compiled {exe.name}")



def execute_require(env: Env, require):
    pass

def execute_include(env: Env, include: Include):
    env.includes.append(include.path)
    
def execute_include_all(env: Env, include_all: IncludeAll):
    path = Path(include_all.path)
    if not path.is_dir():
        raise IsNotADirectory(f"{path} is not a directory")
    
    if not path.exists():
        raise DirectoryNotFound(f"{path} not found")
    
    env.includes.append(str(path))
    for file in listdir(str(path)):
        env.includes.append(str(path / file))
