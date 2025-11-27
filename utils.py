import hashlib
import random
import string

def generate_secure_name(base_name, existing_names, length=12):
    """Generate a secure random name that doesn't conflict with existing names"""
    chars = string.ascii_letters + string.digits
    while True:
        random_part = ''.join(random.choice(chars) for _ in range(length))
        full_name = f"{base_name}_{random_part}"
        if full_name not in existing_names:
            return full_name

def calculate_checksum(data):
    """Calculate SHA256 checksum of data"""
    return hashlib.sha256(data.encode()).hexdigest()

def validate_code(code, language):
    """Basic code validation"""
    if not code.strip():
        return False, "Code is empty"
    
    if len(code) > 1000000:  # 1MB limit
        return False, "Code is too large"
    
    # Add more language-specific validations here
    return True, "Valid code"