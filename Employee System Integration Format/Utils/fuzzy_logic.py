from thefuzz import process

def find_best_match(user_input: str, choices: list[str], threshold: int):
    """
    Finds the best match for user_input from a list of choices using fuzzy matching.
    
    Args:
        user_input (str): The input string to match
        choices (list[str]): List of valid choices to match against
        threshold (int): Minimum similarity score (0-100) to consider a match. Default is 80.
    
    Returns:
        str or None: The best matching choice if score >= threshold, otherwise None
    """
    # Handle empty or whitespace-only input - always return None for consistency
    if not user_input or not user_input.strip():
        return user_input
    
    # Handle empty choices list
    if not choices:
        return user_input
    
    # Get the best match and its similarity score (0-100)
    result = process.extractOne(user_input.strip(), choices)
    
    if result:
        best_match, score = result
        
        # Return the match only if it meets the threshold
        if score >= threshold:
            return best_match
    
    # Return None instead of original input for consistency
    return user_input