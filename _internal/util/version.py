

class Version:

    def from_string(version):
        parts = version.split(".")
        if len(parts) != 3:
            raise Exception(f"Invalid version string: {version}")
        return Version(int(parts[0]), int(parts[1]), int(parts[2]))
    
    def __init__(self, major, minor, patch):
        self.major = major
        self.minor = minor
        self.patch = patch

    def __str__(self):
        return f"{self.major}.{self.minor}.{self.patch}"