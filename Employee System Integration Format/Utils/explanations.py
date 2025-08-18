from typing import Final


class Explanations:
    """
    A collection of standardized explanations for employee system features.
    
    This class serves as a centralized repository for user-facing explanations,
    ensuring consistency across the application interface.
    """
    
    # Office Location Configuration
    OFFICE_LOCATION: Final[str] = (
        """When choosing the office location, users have three options: 
        1) Input a specific office location, 
        2) Send home coordinates if working remotely, or 
        3) Decline to provide location (managers only privilege).
        """
    )

    MULTIPLE_OFFICE_LOCATIONS: Final[str] = (
        """
        Ask the user what all numerous office locations the user wants the employee to check in from
        """
    )

    SINGLE_OFFICE_LOCATION: Final[str] = (
        """
        Ask the user the office location to assign for the employee.
        Also ask him if the use wants the employee to checkin from the site.
        """
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

    ADD_EMPLOYEE_ONBOARDING: Final[str] = (
        """
        give the user a bit of explanation on what each field is. Only explain the fields given to you.

        Here is an example:

        Full Name: The Full name of the employee , e.g. John Doe
        """
    )

    REMINDERS: Final[str] = (
        """
        This reminders is for the employee to get reminders for daily check-in and check-out.
        Ask the user if this employee needs reminders for daily check-in and check-out.
        """
    )

    IS_HR: Final[str] = (
        """
        Ask the user if the employee is an HR.
        """
    )
    
    HR_SCOPE: Final[str] = (
        """
        Ask the user if the employee is an HR for the group or the company.
        """
    )