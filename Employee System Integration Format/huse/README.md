# Huse API Integration

This module handles the integration with the Huse app API for employee registration.

## Overview

When a new employee is successfully added to the main database, the system automatically registers them in the Huse app using the provided API endpoint.

## API Endpoints

### Employee Registration
- **URL**: `http://15.185.143.138:5001/api/Users/register`
- **Method**: POST
- **Content-Type**: form-data

### Security Questions
- **URL**: `http://15.185.143.138:5001/api/Questions`
- **Method**: GET
- **Purpose**: Fetch available security questions for user registration

## Required Fields

The API requires the following fields (all marked as required):

1. **name** (string) - Employee's full name
2. **email** (string) - Employee's email address
3. **username** (string) - Unique username for the employee
4. **contact** (string) - Contact number
5. **gender** (string) - Gender (male/female/other)
6. **terms** (string) - Terms acceptance (default: "accepted")
7. **password** (string) - Default password for the employee
8. **securityQuestion** (string) - Security question (fetched from `/api/Questions` endpoint)
9. **securityAnswer** (string) - Security answer (default: "default")

## Authentication

The API uses Bearer token authentication:
```
Authorization: Bearer eyJhbGciOiJIUzUxMiIsInR5cCI6IkpXVCJ9...
```

## Usage

The integration is automatically triggered when an employee is successfully added to the main database. The process:

1. Employee data is extracted from the database
2. Data is formatted according to Huse API requirements
3. API call is made to register the employee
4. Success/failure status is reported back

## Data Mapping

| Database Field | Huse API Field | Notes |
|----------------|----------------|-------|
| `name` | `name` | Full name (first + middle + last) |
| `email_id` | `email` | Employee's email |
| `contact_no` | `contact` | Contact number |
| `gender` | `gender` | Mapped to male/female/other |
| - | `username` | Generated from email or name |
| - | `password` | Auto-generated default password |
| - | `terms` | Set to "accepted" |
| - | `securityQuestion` | Fetched from `/api/Questions` endpoint |
| - | `securityAnswer` | Default answer |

## Error Handling

The integration includes comprehensive error handling:

- Network errors
- API response errors
- Data validation errors
- Missing required fields (with fallback values)

## Testing

Use the test scripts to verify the integration:

```bash
# Test basic integration
python test_huse_integration.py

# Test security question fetching
python test_security_question.py
```

## Configuration

The API configuration is in `huse/backend.py`:

- Base URL: `http://15.185.143.138:5001`
- Token: Bearer token for authentication
- Default values for required fields

## Logging

The integration includes detailed logging for debugging:

- API request data
- API response status and content
- Error details
- Success confirmation

## Security Notes

- Default passwords should be changed by users after first login
- Security questions and answers are set to defaults
- The Bearer token should be kept secure
- Consider implementing password policies for generated passwords
