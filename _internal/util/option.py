

class Option:
    def __init__(self, value):
        self.value = value

    def is_none(self):
        return self.value is None
    
    def is_some(self):
        return self.value is not None
    
    def unwrap(self):
        if self.is_none():
            raise Exception("Option is None")
        return self.value
    
    def expect(self, msg):
        if self.is_none():
            raise Exception(msg)
        return self.value
    
    def unwrap_or(self, default):
        if self.is_none():
            return default
        return self.value
    
    def map(self, fn):
        if self.is_none():
            return Option(None)
        return Option(fn(self.value))
    
    def map_or(self, default, fn):
        if self.is_none():
            return default
        return fn(self.value)
    
    def map_or_else(self, default, fn):
        if self.is_none():
            return default()
        
        return fn(self.value)
    
    def and_then(self, fn):
        if self.is_none():
            return Option(None)
        return fn(self.value)
    
    def or_else(self, fn):
        if self.is_none():
            return fn()
        return self.value
    
    def __str__(self):
        if self.is_none():
            return "None"
        return f"Some({self.value})"