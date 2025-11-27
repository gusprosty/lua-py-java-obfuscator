import random
import string
import re
import ast
import base64

class PythonObfuscator:
    def __init__(self):
        self.used_names = set()
        
    def generate_random_name(self, length=8):
        chars = string.ascii_letters
        while True:
            name = ''.join(random.choice(chars) for _ in range(length))
            if name not in self.used_names:
                self.used_names.add(name)
                return name
                
    def obfuscate_string(self, s):
        """Obfuscate strings using base64 encoding"""
        encoded = base64.b64encode(s.encode()).decode()
        return f"__import__('base64').b64decode('{encoded}').decode()"
        
    def remove_comments(self, code):
        """Remove single-line comments"""
        lines = code.split('\n')
        cleaned_lines = []
        for line in lines:
            # Remove inline comments but preserve string literals
            in_string = False
            string_char = None
            new_line = []
            
            for i, char in enumerate(line):
                if char in ['"', "'"] and not in_string:
                    in_string = True
                    string_char = char
                    new_line.append(char)
                elif char == string_char and in_string:
                    in_string = False
                    string_char = None
                    new_line.append(char)
                elif char == '#' and not in_string:
                    break
                else:
                    new_line.append(char)
                    
            cleaned_lines.append(''.join(new_line))
            
        return '\n'.join(cleaned_lines)
        
    def obfuscate(self, code, options):
        obfuscated_code = code
        
        if options.get('remove_comments', True):
            obfuscated_code = self.remove_comments(obfuscated_code)
            
        if options.get('obfuscate_strings', True):
            # Find and obfuscate string literals
            string_pattern = r'\"(?:\\.|[^\"])*\"|\'(?:\\.|[^\'])*\''
            strings = re.findall(string_pattern, obfuscated_code)
            
            for s in strings:
                # Don't obfuscate very short strings or docstrings
                if len(s) > 4 and not s.startswith('"""') and not s.startswith("'''"):
                    content = s[1:-1]
                    obfuscated_s = self.obfuscate_string(content)
                    obfuscated_code = obfuscated_code.replace(s, obfuscated_s)
                    
        if options.get('rename_variables', True):
            # Simple variable renaming
            var_pattern = r'\b([a-z_][a-z0-9_]*)\s*='
            variables = re.findall(var_pattern, obfuscated_code, re.IGNORECASE)
            
            var_map = {}
            reserved_words = ['def', 'class', 'if', 'else', 'for', 'while', 'import', 'from', 'return', 'print']
            
            for var in variables:
                if var.lower() not in reserved_words and not var.startswith('__'):
                    if var not in var_map:
                        var_map[var] = self.generate_random_name()
                        
            for old_var, new_var in var_map.items():
                obfuscated_code = re.sub(r'\b' + re.escape(old_var) + r'\b', new_var, obfuscated_code)
                
        if options.get('encrypt_code', False):
            # Add base64 encoding wrapper
            encoded = base64.b64encode(obfuscated_code.encode()).decode()
            wrapper = f"""
import base64
exec(base64.b64decode('{encoded}').decode())
"""
            obfuscated_code = wrapper
            
        return obfuscated_code