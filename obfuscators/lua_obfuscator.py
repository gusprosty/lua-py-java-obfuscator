import random
import string
import re

class LuaObfuscator:
    def __init__(self):
        self.used_names = set()
        
    def generate_random_name(self, length=8):
        chars = string.ascii_letters + string.digits
        while True:
            name = ''.join(random.choice(chars) for _ in range(length))
            if name not in self.used_names and not name[0].isdigit():
                self.used_names.add(name)
                return name
                
    def obfuscate_string(self, s):
        """Obfuscate strings by encoding them"""
        result = []
        for char in s:
            if char.isalnum():
                result.append(f"\\{ord(char):03d}")
            else:
                result.append(char)
        return ''.join(result)
        
    def remove_comments(self, code):
        """Remove single-line and multi-line comments"""
        # Remove single-line comments
        code = re.sub(r'--.*$', '', code, flags=re.MULTILINE)
        # Remove multi-line comments
        code = re.sub(r'--\[\[.*?\]\]', '', code, flags=re.DOTALL)
        return code
        
    def obfuscate(self, code, options):
        obfuscated_code = code
        
        if options.get('remove_comments', True):
            obfuscated_code = self.remove_comments(obfuscated_code)
            
        if options.get('obfuscate_strings', True):
            # Find and obfuscate strings
            string_pattern = r'\"(?:\\.|[^\"])*\"|\'(?:\\.|[^\'])*\''
            strings = re.findall(string_pattern, obfuscated_code)
            
            for s in strings:
                obfuscated_s = self.obfuscate_string(s[1:-1])
                obfuscated_code = obfuscated_code.replace(s, f'"{obfuscated_s}"')
                
        if options.get('rename_variables', True):
            # Simple variable renaming (this is a basic implementation)
            var_pattern = r'\b([a-zA-Z_][a-zA-Z0-9_]*)\s*='
            variables = re.findall(var_pattern, obfuscated_code)
            
            var_map = {}
            for var in variables:
                if var not in ['local', 'function', 'end', 'if', 'else', 'then', 'for', 'while', 'do', 'return']:
                    if var not in var_map:
                        var_map[var] = self.generate_random_name()
                        
            for old_var, new_var in var_map.items():
                obfuscated_code = re.sub(r'\b' + re.escape(old_var) + r'\b', new_var, obfuscated_code)
                
        if options.get('encrypt_code', False):
            # Add basic encryption wrapper
            wrapper = """
local function decode(s)
    local result = ""
    for i = 1, #s do
        result = result .. string.char(string.byte(s, i) - 1)
    end
    return result
end

local encoded = "%s"
local code = decode(encoded)
loadstring(code)()
"""
            # Simple character shift encryption
            encoded = ''.join(chr(ord(c) + 1) for c in obfuscated_code)
            obfuscated_code = wrapper % encoded
            
        return obfuscated_code