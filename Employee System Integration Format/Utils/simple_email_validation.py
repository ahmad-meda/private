from typing import List, Dict, Any

def check_email_send_success(email_results: Dict[str, Any]) -> Dict[str, Any]:
    """
    Check if emails were sent successfully and return failed emails.
    
    Args:
        email_results: Results from email sending function
        
    Returns:
        Dict with success status and failed emails list
    """
    if not email_results:
        return {
            'all_sent': False,
            'failed_emails': [],
            'message': 'No email results provided'
        }
    
    # Check if all emails were sent successfully
    all_sent = email_results.get('success', False)
    failed_emails = email_results.get('failed_emails', [])
    
    return {
        'all_sent': all_sent,
        'failed_emails': failed_emails,
        'sent_to': email_results.get('sent_to', []),
        'message': email_results.get('message', '')
    }

def get_failed_emails_from_send_result(email_results: Dict[str, Any]) -> List[str]:
    """
    Get list of emails that failed to send.
    
    Args:
        email_results: Results from email sending function
        
    Returns:
        List of emails that failed to send
    """
    return email_results.get('failed_emails', [])

# Email format validation functions removed - only checking send success now
