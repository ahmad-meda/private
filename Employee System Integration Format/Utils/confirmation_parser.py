import re
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
from .stopwords import (
    POSITIVE_CONFIRMATIONS, NEGATIVE_CONFIRMATIONS, EDITING_INDICATORS,
    WRONG_EMPLOYEE_INDICATORS, UNRELATED_INDICATORS, EMPLOYEE_FIELDS,
    FAREWELL_MESSAGES, FIELD_MAPPING, FIELD_VALUE_PATTERNS
)

@dataclass
class ConfirmationIntent:
    """Data class to represent the parsed confirmation intent"""
    does_user_want_to_update: bool
    did_user_mention_editing: bool
    is_wrong_employee: bool
    is_unrelated_response: bool
    farewell_message: str
    additional_fields: Dict[str, str]  # Fields mentioned in addition to confirmation

class ConfirmationParser:
    """Parser for user confirmation responses using stopwords and regex patterns"""
    
    def __init__(self):
        # Use stopwords from the separate file
        self.positive_confirmations = POSITIVE_CONFIRMATIONS
        self.negative_confirmations = NEGATIVE_CONFIRMATIONS
        self.editing_indicators = EDITING_INDICATORS
        self.wrong_employee_indicators = WRONG_EMPLOYEE_INDICATORS
        self.unrelated_indicators = UNRELATED_INDICATORS
        self.employee_fields = EMPLOYEE_FIELDS
        self.farewell_messages = FAREWELL_MESSAGES
        self.field_mapping = FIELD_MAPPING
        self.field_value_patterns = FIELD_VALUE_PATTERNS
    
    def parse_confirmation_response(self, user_message: str) -> ConfirmationIntent:
        """
        Parse user's confirmation response and determine intent
        
        Args:
            user_message: The user's response to confirmation
            
        Returns:
            ConfirmationIntent object with parsed intent
        """
        # Normalize the message
        normalized_message = self._normalize_message(user_message)
        
        # Check for different intents
        is_positive = self._check_positive_confirmation(normalized_message)
        is_negative = self._check_negative_confirmation(normalized_message)
        is_editing = self._check_editing_intent(normalized_message)
        is_wrong_employee = self._check_wrong_employee(normalized_message)
        is_unrelated = self._check_unrelated_response(normalized_message)
        
        # Extract additional fields if user mentions them
        additional_fields = self._extract_additional_fields(normalized_message)
        
        # Determine the primary intent
        if is_unrelated:
            return ConfirmationIntent(
                does_user_want_to_update=False,
                did_user_mention_editing=False,
                is_wrong_employee=False,
                is_unrelated_response=True,
                farewell_message=self.farewell_messages['unrelated'],
                additional_fields={}
            )
        
        if is_wrong_employee:
            return ConfirmationIntent(
                does_user_want_to_update=False,
                did_user_mention_editing=False,
                is_wrong_employee=True,
                is_unrelated_response=False,
                farewell_message="",
                additional_fields={}
            )
        
        if is_editing or additional_fields:
            return ConfirmationIntent(
                does_user_want_to_update=is_positive,  # True if they said yes AND want to edit
                did_user_mention_editing=True,
                is_wrong_employee=False,
                is_unrelated_response=False,
                farewell_message="",
                additional_fields=additional_fields
            )
        
        if is_negative:
            return ConfirmationIntent(
                does_user_want_to_update=False,
                did_user_mention_editing=False,
                is_wrong_employee=False,
                is_unrelated_response=False,
                farewell_message=self.farewell_messages['decline'],
                additional_fields={}
            )
        
        if is_positive:
            return ConfirmationIntent(
                does_user_want_to_update=True,
                did_user_mention_editing=False,
                is_wrong_employee=False,
                is_unrelated_response=False,
                farewell_message="",
                additional_fields={}
            )
        
        # Default case - unclear response
        return ConfirmationIntent(
            does_user_want_to_update=False,
            did_user_mention_editing=False,
            is_wrong_employee=False,
            is_unrelated_response=False,
            farewell_message=self.farewell_messages['unclear'],
            additional_fields={}
        )
    
    def _normalize_message(self, message: str) -> str:
        """Normalize the message for pattern matching"""
        # Convert to lowercase
        normalized = message.lower().strip()
        
        # Remove extra whitespace
        normalized = re.sub(r'\s+', ' ', normalized)
        
        # Remove punctuation at the end
        normalized = re.sub(r'[.!?]+$', '', normalized)
        
        return normalized
    
    def _check_positive_confirmation(self, message: str) -> bool:
        """Check if message contains positive confirmation"""
        words = set(message.split())
        return bool(words.intersection(self.positive_confirmations))
    
    def _check_negative_confirmation(self, message: str) -> bool:
        """Check if message contains negative confirmation"""
        words = set(message.split())
        return bool(words.intersection(self.negative_confirmations))
    
    def _check_editing_intent(self, message: str) -> bool:
        """Check if user wants to edit/modify details"""
        words = set(message.split())
        return bool(words.intersection(self.editing_indicators))
    
    def _check_wrong_employee(self, message: str) -> bool:
        """Check if user is referring to wrong employee"""
        for indicator in self.wrong_employee_indicators:
            if indicator in message:
                return True
        return False
    
    def _check_unrelated_response(self, message: str) -> bool:
        """Check if response is unrelated to confirmation"""
        words = set(message.split())
        return bool(words.intersection(self.unrelated_indicators))
    
    def _extract_additional_fields(self, message: str) -> Dict[str, str]:
        """Extract additional fields mentioned in the message"""
        additional_fields = {}
        
        # Use patterns from stopwords file
        for pattern in self.field_value_patterns:
            matches = re.findall(pattern, message, re.IGNORECASE)
            for field, value in matches:
                field = field.strip().lower()
                value = value.strip()
                
                # Check if the field is a valid employee field
                if any(emp_field in field for emp_field in self.employee_fields):
                    # Map common field names to standard names
                    mapped_field = self._map_field_name(field)
                    additional_fields[mapped_field] = value
        
        return additional_fields
    
    def _map_field_name(self, field: str) -> str:
        """Map common field names to standard field names"""
        return self.field_mapping.get(field, field)


# Convenience function for easy import
def parse_confirmation_response(user_message: str) -> ConfirmationIntent:
    """
    Convenience function to parse confirmation response
    
    Args:
        user_message: The user's response to confirmation
        
    Returns:
        ConfirmationIntent object with parsed intent
    """
    parser = ConfirmationParser()
    return parser.parse_confirmation_response(user_message)
