from typing import Final


class Explanations:
    """
    A collection of standardized explanations for employee system features.
    
    This class serves as a centralized repository for user-facing explanations,
    ensuring consistency across the application interface.
    """
    
    # Office Location Configuration
    OFFICE_LOCATION: Final[str] = (
        "When choosing the office location, users have three options: "
        "1) Input a specific office location, "
        "2) Send home coordinates if working remotely, or "
        "3) Decline to provide location (managers only privilege)."
    )
    
    # Attendance Management System
    ATTENDANCE_TRACKING: Final[str] = (
        "Employee attendance tracking supports flexible work arrangements. "
        "Employees can mark their status as: office presence, remote work, "
        "or scheduled leave with appropriate documentation."
    )
    
    # Role-Based Access Control
    ROLE_PERMISSIONS: Final[str] = (
        "Employee roles determine system access levels and capabilities. "
        "Standard employees have basic functionality access, while managers "
        "receive additional privileges including team oversight and "
        "privacy configuration options."
    )
    
    # Data Privacy & Security
    DATA_PRIVACY: Final[str] = (
        "All employee data is handled in accordance with privacy regulations. "
        "Personal information access is restricted based on role hierarchy "
        "and business necessity principles."
    )