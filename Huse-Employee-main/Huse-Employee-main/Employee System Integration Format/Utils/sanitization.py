from datetime import datetime


def as_str(val):
    if isinstance(val, (datetime.datetime, datetime.date)):
        return val.isoformat()
    return str(val)

def sanitize_messages(msgs):
    # Only allow role and content, both as strings
    return [
        {
            "role": str(msg.get("role", "")),
            "content": str(msg.get("content", ""))
        }
        for msg in msgs
    ]