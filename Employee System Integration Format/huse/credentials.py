import random
import string
import re
import bcrypt
import os
from typing import Tuple
from sqlalchemy.orm import Session
from proxies.proxy import EmployeeProxy
from Utils.password_helpers import generate_username, generate_password, hash_password, split_name, check_username_exists
from helpers.username_validation import get_all_usernames_from_api


def generate_credentials(employee_name: str, db_session: Session = None) -> Tuple[str, str, str]:
    """
    Generate username, plain password, and encrypted password for an employee.
    
    This function ensures username uniqueness by checking the database and generating
    alternative usernames if the initial one already exists.
    
    Args:
        employee_name: Full name of the employee
        db_session: Database session to check for existing usernames
        
    Returns:
        Tuple of (username, plain_password, encrypted_password)
    """
    first_name, last_name = split_name(employee_name)
    
    # Generate initial username from employee name
    username = generate_username(first_name, last_name)
    attempts = 0
    
    # This is to ensure username uniqueness by checking database and Huse API and regenerating if needed
    # This prevents conflicts when multiple employees have similar names
    # Example: "John Doe" -> "jdoe", if exists -> "john.doe", if exists -> "jdoe123"
    while (check_username_exists(username) or username in get_all_usernames_from_api()) and attempts < 10:
        username = generate_username(first_name, last_name)  # Generate alternative username
        attempts += 1  # This to prevent infinite loops by limiting attempts
    
    # This is to generate a secure password (bcrypt handles uniqueness automatically)
    plain_password = generate_password()
    
    # We are hashing the password for secure storage
    encrypted_password = hash_password(plain_password)
    
    return username, plain_password, encrypted_password


def generate_security_answer(employee_name: str, employee_id: str = None) -> str:
    """
    Generate a unique security answer based on the employee's name and ID.
    
    This creates a unique answer that can be used for security questions.
    The answer is based on the employee's name and includes the employee ID to ensure uniqueness.
    
    Args:
        employee_name: Full name of the employee
        employee_id: Unique employee ID (optional, will generate random if not provided)
        
    Returns:
        A unique security answer string
    """
    # Clean and split the name
    name_parts = employee_name.strip().split()
    
    # Generate a unique identifier if employee_id is not provided
    if not employee_id:
        # Use a combination of name hash and random elements for uniqueness
        import hashlib
        import time
        name_hash = hashlib.md5(employee_name.encode()).hexdigest()[:6]
        timestamp = str(int(time.time() * 1000))[-4:]  # Last 4 digits of timestamp
        unique_id = f"{name_hash}{timestamp}"
    else:
        unique_id = str(employee_id)
    
    if len(name_parts) >= 2:
        # Use first and last name with the unique identifier
        first_name = name_parts[0].lower()
        last_name = name_parts[-1].lower()
        
        # Generate the security answer and truncate to 25 characters max
        security_answer = f"{first_name}{last_name}{unique_id}"[:25]
        
    elif len(name_parts) == 1:
        # Single name - use it with the unique identifier
        name = name_parts[0].lower()
        security_answer = f"{name}{unique_id}"[:25]
        
    else:
        # Fallback for empty names
        security_answer = f"user{unique_id}"[:25]
    
    return security_answer