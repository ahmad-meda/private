import random
import string
import re
import bcrypt
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
    """Generate username from name."""
    first_initial = first_name[0].lower()
    last_name_lower = last_name.lower()
    
    # Try different username patterns
    patterns = [
        f"{first_initial}{last_name_lower}",
        f"{first_name.lower()}.{last_name_lower}",
        f"{first_name.lower()}{last_name_lower}",
        f"{first_initial}{last_name_lower}{random.randint(100, 999)}",
        f"{first_name.lower()}{random.randint(100, 999)}"
    ]
    
    for pattern in patterns:
        if len(pattern) <= 20:  # Max length
            return pattern
    
    # Fallback
    return f"{first_initial}{last_name_lower}{random.randint(100, 999)}"

def generate_password() -> str:
    """Generate a strong password."""
    # Ensure all character types are included
    password = [
        random.choice(string.ascii_uppercase),  # Uppercase
        random.choice(string.ascii_lowercase),  # Lowercase
        random.choice(string.digits),           # Digit
        random.choice("!@#$%^&*()_+-=[]{}|;:,.<>?")  # Special char
    ]
    
    # Add more random characters to reach minimum length
    all_chars = string.ascii_letters + string.digits + "!@#$%^&*()_+-=[]{}|;:,.<>?"
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
    Hash password using bcrypt.
    
    Args:
        password: The plain text password
        
    Returns:
        Hashed password string
    """
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

def check_password(password: str, hashed: str) -> bool:
    """
    Check if password is correct.
    
    Args:
        password: The plain text password to verify
        hashed: The stored hash
        
    Returns:
        True if password matches, False otherwise
    """
    return bcrypt.checkpw(password.encode(), hashed.encode())