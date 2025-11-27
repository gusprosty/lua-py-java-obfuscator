import random
import string
import re
import base64

class JavaObfuscator:
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
        return f"new String(java.util.Base64.getDecoder().decode(\"{encoded}\"))"
        
    def remove_comments(self, code):
        """Remove single-line and multi-line comments"""
        # Remove single-line comments
        code = re.sub(r'//.*$', '', code, flags=re.MULTILINE)
        # Remove multi-line comments
        code = re.sub(r'/\*.*?\*/', '', code, flags=re.DOTALL)
        return code
        
    def obfuscate(self, code, options):
        obfuscated_code = code
        
        if options.get('remove_comments', True):
            obfuscated_code = self.remove_comments(obfuscated_code)
            
        if options.get('obfuscate_strings', True):
            # Find and obfuscate string literals
            string_pattern = r'\"(?:\\.|[^\"])*\"'
            strings = re.findall(string_pattern, obfuscated_code)
            
            for s in strings:
                # Don't obfuscate very short strings
                if len(s) > 4:
                    content = s[1:-1]
                    obfuscated_s = self.obfuscate_string(content)
                    obfuscated_code = obfuscated_code.replace(s, obfuscated_s)
                    
        if options.get('rename_variables', True):
            # Simple variable renaming
            var_pattern = r'\b([a-zA-Z_][a-zA-Z0-9_]*)\s*='
            variables = re.findall(var_pattern, obfuscated_code)
            
            var_map = {}
            reserved_words = ['public', 'private', 'protected', 'class', 'void', 'int', 'String', 'boolean', 'return']
            
            for var in variables:
                if var not in reserved_words:
                    if var not in var_map:
                        var_map[var] = self.generate_random_name()
                        
            for old_var, new_var in var_map.items():
                obfuscated_code = re.sub(r'\b' + re.escape(old_var) + r'\b', new_var, obfuscated_code)
                
        if options.get('encrypt_code', False):
            # Add basic encryption (this is a simplified example)
            wrapper = """
import java.util.Base64;
public class Obfuscated {{
    public static void main(String[] args) {{
        String encoded = "%s";
        byte[] decoded = Base64.getDecoder().decode(encoded);
        String code = new String(decoded);
        // Note: Actual execution would require more complex setup
        System.out.println("Code would be executed here");
    }}
}}
"""
            encoded = base64.b64encode(obfuscated_code.encode()).decode()
            obfuscated_code = wrapper % encoded
            
        return obfuscated_code
