from datetime import datetime


def as_str(val):
    if isinstance(val, (datetime.datetime, datetime.date)):
        return val.isoformat()
    return str(val)

def sanitize_messages(msgs):
    # Only allow role and content, both as strings
    # Handle nested arrays by flattening them
    flattened_msgs = []
    for msg in msgs:
        if isinstance(msg, list):
            # If it's a list, extend the flattened_msgs with sanitized items from the list
            flattened_msgs.extend([
                {
                    "role": str(item.get("role", "")),
                    "content": str(item.get("content", ""))
                }
                for item in msg if isinstance(item, dict)
            ])
        elif isinstance(msg, dict):
            # If it's a dict, add it directly
            flattened_msgs.append({
                "role": str(msg.get("role", "")),
                "content": str(msg.get("content", ""))
            })
    
    return flattened_msgs