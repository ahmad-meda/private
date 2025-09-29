# Employee System Integration Format

## Overview

This is a comprehensive Employee Management System built with Flask that provides intelligent CRUD operations for employee data through WhatsApp-based conversational AI. The system integrates with HUSE (Human Use System Environment) for user account management and uses advanced AI agents for natural language processing.

## 🏗️ Architecture

The system follows a **layered architecture pattern** with clear separation of concerns:

- **Presentation Layer**: Flask web application with conversational AI interface
- **Business Logic Layer**: AI agents, validation, and business rules
- **Data Access Layer**: Proxy pattern with service layer abstraction
- **Data Layer**: PostgreSQL database with SQLAlchemy ORM
- **Caching Layer**: Redis for session management and temporary data
- **External Integration**: HUSE API for user account management

## 📁 Project Structure

```
Employee System Integration Format/
├── app.py                          # Flask application entry point
├── database.py                     # Database configuration and initialization
├── requirements.txt                # Python dependencies
├── Files/
│   └── SQLAlchemyModels.py        # Database models and schemas
├── proxies/                        # Data access layer (Proxy Pattern)
│   ├── proxy.py                   # Main employee proxy
│   ├── employee_message_proxy.py  # Message history proxy
│   └── employee_session_proxy.py  # Session management proxy
├── services/                       # Business logic layer
│   ├── service.py                 # Core employee service
│   ├── employee_message_service.py # Message service
│   └── employee_session_service.py # Session service
├── Utils/                         # Utility functions and helpers
│   ├── agents.py                  # AI agent implementations
│   ├── ai_client.py              # OpenAI client configuration
│   ├── sanitization.py           # Input sanitization
│   ├── contact_validation.py     # Phone number validation
│   ├── fuzzy_logic.py            # Fuzzy string matching
│   ├── password_helpers.py       # Password generation and hashing
│   └── [other utility modules]
├── huse/                          # HUSE integration
│   ├── backend.py                # HUSE API integration
│   ├── credentials.py            # Credential generation
│   └── email.py                  # Email notification system
├── static/                        # Static assets
│   └── logos/                    # Application logos
└── [CRUD operation files]        # Individual CRUD implementations
    ├── create_employee.py
    ├── get_employee.py
    ├── update_employee.py
    └── delete_employee.py
```

## 🔄 CRUD Operations Flowcharts

### 1. CREATE Employee Operation

```mermaid
flowchart TD
    A[User sends message via WhatsApp] --> B[Save message to PostgreSQL & Redis]
    B --> C[Get HR agent details from contact number]
    C --> D[Create/Get draft record for employee]
    D --> E[Get null fields from employee record]
    E --> F[Get session fields from Redis]
    F --> G[Auto-assign company if no group]
    G --> H[Extract data using AI agent]
    H --> I[Apply fuzzy logic for field matching]
    I --> J[Validate and update draft record]
    J --> K{All mandatory fields filled?}
    K -->|No| L[Ask for missing fields via AI agent]
    L --> M[Send response via WhatsApp]
    M --> A
    K -->|Yes| N[Add employee to main database]
    N --> O[Create leave balances]
    O --> P[Generate HUSE credentials]
    P --> Q[Register employee in HUSE]
    Q --> R[Send credentials via email]
    R --> S[Activate HUSE account]
    S --> T[Clear sessions and send confirmation]
    T --> U[Delete draft record]
```

### 2. READ Employee Operation

```mermaid
flowchart TD
    A[User requests employee data] --> B[Save message to PostgreSQL & Redis]
    B --> C[Get HR agent details]
    C --> D[Extract search criteria using AI]
    D --> E{All search fields provided?}
    E -->|No| F[Ask for missing criteria]
    F --> G[Send response via WhatsApp]
    G --> A
    E -->|Yes| H[Clean and validate search fields]
    H --> I[Execute database queries for each criterion]
    I --> J[Combine results from all queries]
    J --> K[Format employee data]
    K --> L[Generate natural language response]
    L --> M[Send formatted results via WhatsApp]
    M --> N[Clear session data]
```

### 3. UPDATE Employee Operation

```mermaid
flowchart TD
    A[User requests employee update] --> B[Save message to PostgreSQL & Redis]
    B --> C[Get HR agent details]
    C --> D{Employee identified?}
    D -->|No| E[Extract employee identification data]
    E --> F[Apply fuzzy matching for employee name]
    F --> G{Multiple matches found?}
    G -->|Yes| H[Present options to user]
    H --> I[User selects employee]
    I --> J[Set employee as identified]
    G -->|No| K[Set employee as identified]
    D -->|Yes| L[Extract update fields and values]
    J --> L
    K --> L
    L --> M[Apply fuzzy logic for field values]
    M --> N[Validate and update employee record]
    N --> O{Update successful?}
    O -->|No| P[Report errors to user]
    O -->|Yes| Q[Ask if user wants to update more fields]
    P --> R[Send response via WhatsApp]
    Q --> R
    R --> S{User wants to continue?}
    S -->|Yes| A
    S -->|No| T[Clear session and end conversation]
```

### 4. DELETE Employee Operation

```mermaid
flowchart TD
    A[User requests employee deletion] --> B[Save message to PostgreSQL & Redis]
    B --> C[Get HR agent details]
    C --> D[Extract employee identification data]
    D --> E{Employee name provided?}
    E -->|Yes| F[Apply fuzzy matching for employee name]
    F --> G{Multiple matches found?}
    G -->|Yes| H[Present options to user]
    H --> I[User selects employee]
    I --> J[Perform soft delete]
    G -->|No| J
    E -->|No| K{Contact number provided?}
    K -->|Yes| L[Find employee by contact number]
    L --> J
    K -->|No| M[Ask for employee identification]
    M --> N[Send response via WhatsApp]
    N --> A
    J --> O{Delete successful?}
    O -->|Yes| P[Send confirmation message]
    O -->|No| Q[Report error message]
    P --> R[Clear session data]
    Q --> R
```

## 🛡️ Security Measures & Precautions

### 1. **Input Validation & Sanitization**
- **Message Sanitization**: All user messages are sanitized to prevent injection attacks
- **Contact Number Validation**: International phone number validation using `phonenumbers` library
- **Field Validation**: Comprehensive validation for all employee fields before database operations
- **SQL Injection Prevention**: Using SQLAlchemy ORM with parameterized queries

### 2. **Authentication & Authorization**
- **HR Agent Verification**: System verifies HR agent identity through contact number lookup
- **Company/Group Scoping**: All operations are scoped to the HR agent's company and group
- **Access Control**: Employees can only be managed within the HR agent's organizational scope

### 3. **Password Security**
- **Strong Password Generation**: 12-character passwords with uppercase, lowercase, digits, and special characters
- **Password Hashing**: SHA-256 hashing for secure password storage
- **Username Uniqueness**: Automatic username generation with collision detection
- **Credential Management**: Secure credential generation and storage for HUSE integration

### 4. **Data Protection**
- **Soft Delete**: Employee deletion is soft delete (marking as deleted, not removing data)
- **Draft System**: Employee creation uses draft system to prevent incomplete records
- **Session Management**: Redis-based session management with automatic cleanup
- **Data Encryption**: Sensitive data is properly handled and encrypted where necessary

### 5. **Error Handling**
- **Comprehensive Error Catching**: All database operations wrapped in try-catch blocks
- **Graceful Degradation**: System continues to function even if some operations fail
- **Error Logging**: Detailed error logging for debugging and monitoring
- **User-Friendly Error Messages**: Errors are translated to user-friendly messages

### 6. **API Security**
- **Environment Variables**: Sensitive configuration stored in environment variables
- **Token-Based Authentication**: HUSE API integration uses secure token authentication
- **Request Validation**: All API requests are validated before processing
- **Rate Limiting**: Built-in protection against rapid successive requests

## 🔧 Key Features & Implementations

### 1. **AI-Powered Conversational Interface**
- **Natural Language Processing**: Uses OpenAI GPT-4 for understanding user intent
- **Context Awareness**: Maintains conversation context across multiple interactions
- **Intelligent Field Extraction**: Automatically extracts relevant data from natural language
- **Fuzzy Matching**: Handles typos and variations in user input

### 2. **Advanced Data Management**
- **Draft System**: Prevents incomplete employee records from being created
- **Field Validation**: Comprehensive validation for all employee fields
- **Relationship Management**: Proper handling of foreign key relationships
- **Data Consistency**: Ensures data integrity across all operations

### 3. **Session Management**
- **Redis Integration**: Fast session storage and retrieval
- **Message History**: Maintains conversation history for context
- **Field Tracking**: Tracks which fields have been collected
- **Automatic Cleanup**: Sessions are automatically cleaned up after operations

### 4. **HUSE Integration**
- **Automatic Account Creation**: Creates user accounts in HUSE system
- **Credential Generation**: Generates secure usernames and passwords
- **Email Notifications**: Sends credentials to both employee and HR
- **Status Management**: Manages account activation and status updates

### 5. **Multi-Company Support**
- **Company Scoping**: All operations are scoped to specific companies
- **Group Management**: Supports organizational group structures
- **Hierarchical Access**: Respects organizational hierarchy in data access

## 🚀 Getting Started

### Prerequisites
- Python 3.8+
- PostgreSQL database
- Redis server
- OpenAI API key
- HUSE API credentials

### Installation

1. **Clone the repository**
```bash
git clone <repository-url>
cd "Employee System Integration Format"
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Set up environment variables**
```bash
# Create .env file with the following variables:
DATABASE_URL=postgresql://username:password@localhost:5432/Employee
REDIS_URL=redis://localhost:6379
OPENAI_API_KEY=your_openai_api_key
API_BASE_URL=your_huse_api_base_url
API_AUTH_TOKEN=your_huse_auth_token
FLASK_DEBUG=0

# Email configuration (Mandrill)
MANDRILL_API_KEY=your_mandrill_api_key
EMAIL_SENDER_ADDRESS=no-reply@huse.ai
EMAIL_SENDER_NAME=Huse Team
```

4. **Initialize the database**
```bash
flask db init
flask db migrate
flask db upgrade
```

5. **Run the application**
```bash
python app.py
```

## 📊 Database Schema

The system uses the following main entities:
- **Employee**: Core employee information
- **EmployeeDraft**: Temporary employee data during creation
- **Company**: Company information
- **Department**: Department information
- **Role**: Employee roles
- **WorkPolicy**: Work policy definitions
- **OfficeLocation**: Office location data
- **Group**: Organizational groups
- **Draft**: Draft management system
- **HuseApp**: HUSE integration data

## 🔄 Data Flow

1. **User Input**: User sends message via WhatsApp
2. **Message Processing**: System processes and sanitizes input
3. **AI Analysis**: AI agent extracts relevant information
4. **Validation**: Data is validated against business rules
5. **Database Operations**: CRUD operations are performed
6. **External Integration**: HUSE system is updated if needed
7. **Response Generation**: AI generates natural language response
8. **User Notification**: Response is sent back to user

## 🛠️ Technology Stack

- **Backend**: Flask (Python)
- **Database**: PostgreSQL with SQLAlchemy ORM
- **Caching**: Redis
- **AI/ML**: OpenAI GPT-4
- **Email**: SMTP integration
- **Validation**: Pydantic models
- **Fuzzy Matching**: TheFuzz library
- **Phone Validation**: phonenumbers library
- **Password Security**: bcrypt, hashlib

## 📝 API Endpoints

The system provides the following main operations:
- `create_employee()`: Create new employee
- `get_employee_records()`: Search and retrieve employee data
- `update_employee_fields()`: Update existing employee information
- `soft_delete_employee()`: Soft delete employee record

## 🔍 Monitoring & Logging

- **Comprehensive Logging**: All operations are logged for debugging
- **Error Tracking**: Detailed error information for troubleshooting
- **Performance Monitoring**: Session and operation timing
- **Audit Trail**: Complete audit trail of all employee operations

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For support and questions, please contact the development team or create an issue in the repository.

---

**Note**: This system is designed for enterprise use and includes comprehensive security measures, error handling, and data validation to ensure reliable and secure employee management operations.
