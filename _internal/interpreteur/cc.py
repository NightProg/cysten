import subprocess

class CC:
    def __init__(self, cc) -> None:
        self.cc = cc 
        self.flags = []
        self.commands = []
        self.output = None
        self.includes = []
        self.links = []
        self.files = []

    def __str__(self) -> str:
        commands = " ".join(self.commands)
        output = self.output if self.output else ""
        includes = " ".join(self.includes)
        flags = " ".join(self.flags)
        links = " ".join(self.links)
        files = " ".join(self.files)
        s = str(self.cc) + " "
        if len(self.flags):
            s += flags + " "
        
        if len(self.commands):
            s += commands + ""

        if self.output:
            s += "-o " + output + " "
        
        if len(self.includes):
            s += "-I " + includes + " "
        
        if len(self.links):
            s += "-L " + links + " "

        if len(self.files):
            s += files 

        return s
    
    def execute(self):
        commands = [self.cc, *self.files]
        if self.output:
            commands.extend(["-o", self.output])
        if len(self.includes):
            commands.extend(["-I", *self.includes])
        if len(self.links):
            commands.extend(self.links)
        
        if len(self.commands):
            commands.extend(self.commands)
        
        return subprocess.run(commands)

    