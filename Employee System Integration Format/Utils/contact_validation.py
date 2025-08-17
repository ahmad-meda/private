import phonenumbers
from phonenumbers.phonenumberutil import NumberParseException

def is_valid_international(num_digits: str) -> bool:
    """
    Expects only digits.
    • Adds "+" so phonenumbers can parse.
    • Checks both:  ✔ country code exists  ✔ length rule for that country.
    """
    try:
        obj = phonenumbers.parse("+" + num_digits, None)  # None = infer region from country code
        print(phonenumbers.region_code_for_number(obj))
        return phonenumbers.is_valid_number(obj)
    except NumberParseException:
        return False