import random
import string
import re
import hashlib
from typing import Tuple
from proxies.proxy import EmployeeProxy

def clean_name(name: str) -> str:
    """Clean and normalize name."""
    cleaned = re.sub(r'[^a-zA-Z\s]', '', name.strip())
    cleaned = re.sub(r'\s+', ' ', cleaned)
    return cleaned

def split_name(name: str) -> Tuple[str, str]:
    """Split name into first and last."""
    parts = clean_name(name).split()
    if len(parts) == 1:
        return parts[0], "User"
    elif len(parts) == 2:
        return parts[0], parts[1]
    else:
        return parts[0], parts[-1]

def generate_username(first_name: str, last_name: str) -> str:
    """Generate username from first 4 letters of first name and last 4 letters of last name."""
    first_name_clean = clean_name(first_name).lower()
    last_name_clean = clean_name(last_name).lower()
    
    # Get first 4 letters of first name, or all if less than 4
    first_4 = first_name_clean[:4] if len(first_name_clean) >= 4 else first_name_clean.ljust(4, 'x')
    
    # Get first 4 letters of last name, or all if less than 4
    last_4 = last_name_clean[:4] if len(last_name_clean) >= 4 else last_name_clean.rjust(4, 'x')
    
    # Combine them
    base_username = f"{first_4}{last_4}"
    
    # If username already exists, add random numbers
    if check_username_exists(base_username):
        return f"{base_username}{random.randint(1, 99)}"
    
    return base_username

def generate_password() -> str:
    """Generate a strong password."""
    # Ensure all character types are included
    password = [
        random.choice(string.ascii_uppercase),  # Uppercase
        random.choice(string.ascii_lowercase),  # Lowercase
        random.choice(string.digits),           # Digit
        random.choice("!@#$%^&*_+-=|:,.?")  # Special char
    ]
    
    # Add more random characters to reach minimum length
    all_chars = string.ascii_letters + string.digits + "!@#$%^&*_+-=|:,.?"
    for _ in range(8):  # Total length will be 12
        password.append(random.choice(all_chars))
    
    # Shuffle the password
    random.shuffle(password)
    return ''.join(password)

def check_username_exists(username: str) -> bool:
    """Check if username exists in database."""
    return EmployeeProxy.check_username_exists(username)



def hash_password(password: str) -> str:
    """
    Hash password using SHA-256.
    
    Args:
        password: The plain text password
        
    Returns:
        Hashed password string
    """
    return hashlib.sha256(password.encode()).hexdigest()

def check_password(password: str, hashed: str) -> bool:
    """
    Check if password is correct.
    
    Args:
        password: The plain text password to verify
        hashed: The stored hash
        
    Returns:
        True if password matches, False otherwise
    """
    password_hash = hashlib.sha256(password.encode()).hexdigest()
    return password_hash == hashed