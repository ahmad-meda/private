from pydantic import BaseModel
from flask import jsonify, request, Flask
from pydantic import ValidationError
from crm_huse import crm_to_huse
from dotenv import load_dotenv
from huse_email import send_employee_credentials_email
import os

load_dotenv()
API_KEY = os.getenv("HUSE_API_KEY")
from flask import Flask
from flasgger import Swagger
from typing import Optional

app = Flask(__name__)
swagger = Swagger(app)
app.config['JSON_SORT_KEYS'] = False

class CrmToHuseData(BaseModel):
    name: str
    phone: str
    email: str
    suggested_membership_tier: str
    lead_status: str
    company: Optional[str] = None
    preferred_nickname: Optional[str] = None
    date_of_birth: Optional[str] = None
    nationality: Optional[str] = None
    residential_address: Optional[str] = None
    passport_number: Optional[str] = None
    id_number: Optional[str] = None
    occupation: Optional[str] = None
    job_title: Optional[str] = None
    linkedin_or_website: Optional[str] = None
    education_background: Optional[str] = None
    notable_affiliations: Optional[str] = None
    lead_comments: Optional[str] = None
    approval_status: Optional[str] = None
    crm_backend_id: Optional[str] = None
    status: Optional[str] = None


@app.route("/crm_to_huse", methods=["POST"])
def crm_to_huse_api():
    """
    Add a lead directly to Huse database
    ---
    tags:
      - leads
    parameters:
      - name: huse-api-key
        in: header
        type: string
        required: true
        description: API key for authentication
      - name: body
        in: body
        required: true
        description: Lead information for Huse database
        schema:
          type: object
          properties:
            name:
              type: string
              description: Full legal name
            phone:
              type: string
              description: Phone number
            email:
              type: string
              description: Email address
            suggested_membership_tier:
              type: string
              description: Suggested membership tier
            company:
              type: string
              description: Company name
            lead_status:
              type: string
              description: Lead status
            preferred_nickname:
              type: string
              description: Preferred nickname (optional)
            date_of_birth:
              type: string
              description: Date of birth (optional)
            nationality:
              type: string
              description: Nationality (optional)
            residential_address:
              type: string
              description: Residential address (optional)
            passport_number:
              type: string
              description: Passport number (optional)
            id_number:
              type: string
              description: ID number (optional)
            occupation:
              type: string
              description: Occupation (optional)
            job_title:
              type: string
              description: Job title (optional)
            linkedin_or_website:
              type: string
              description: LinkedIn or website (optional)
            education_background:
              type: string
              description: Education background (optional)
            notable_affiliations:
              type: string
              description: Notable affiliations (optional)
            lead_comments:
              type: string
              description: Lead comments (optional)
            approval_status:
              type: string
              description: Approval status (optional)
            crm_backend_id:
              type: string
              description: CRM backend ID (optional)
            status:
              type: string
              description: Status (optional)
          required:
            - name
            - phone
            - email
            - suggested_membership_tier
            - lead_status
    responses:
      200:
        description: Lead added successfully to Huse database
        schema:
          type: object
          properties:
            message:
              type: string
            huse_response:
              type: object
      400:
        description: Bad request - validation error or missing data
        schema:
          type: object
          properties:
            error:
              type: string
            details:
              type: array
              items:
                type: object
      401:
        description: Unauthorized - invalid or missing API key
        schema:
          type: object
          properties:
            error:
              type: string
              example: "Unauthorized"
      500:
        description: Internal server error
        schema:
          type: object
          properties:
            error:
              type: string
              example: "Internal server error: ..."
    """
    try:
        # Check API key authentication
        api_key = request.headers.get("huse-api-key")
        if api_key != API_KEY:
            return jsonify({"error": "Unauthorized"}), 401
            
        # Get JSON data from request
        json_data = request.get_json()
        
        if not json_data:
            return jsonify({"error": "No JSON data provided"}), 400
        
        # Validate using Pydantic model
        try:
            lead_data = CrmToHuseData(**json_data)
        except ValidationError as e:
            return jsonify({
                "error": "Validation failed",
                "details": e.errors()
            }), 400
            
        print(f"Adding lead to Huse database: {lead_data.name}")
        
        # Call crm_to_huse function with all parameters
        huse_response = crm_to_huse(
            name=lead_data.name,
            phone=lead_data.phone,
            email=lead_data.email,
            suggested_membership_tier=lead_data.suggested_membership_tier,
            company=lead_data.company,
            lead_status=lead_data.lead_status,
            preferred_nickname=lead_data.preferred_nickname,
            date_of_birth=lead_data.date_of_birth,
            nationality=lead_data.nationality,
            residential_address=lead_data.residential_address,
            passport_number=lead_data.passport_number,
            id_number=lead_data.id_number,
            occupation=lead_data.occupation,
            job_title=lead_data.job_title,
            linkedin_or_website=lead_data.linkedin_or_website,
            education_background=lead_data.education_background,
            notable_affiliations=lead_data.notable_affiliations,
            lead_comments=lead_data.lead_comments,
            approval_status=lead_data.approval_status,
            crm_backend_id=lead_data.crm_backend_id,
            status=lead_data.status
        )
        
        # Check if the response indicates failure
        if isinstance(huse_response, dict) and huse_response.get("failure"):
            return jsonify({
                "error": huse_response.get("error", "Failed to add lead to Huse database")
            }), 400
        
        return jsonify({
            "message": "Successfully added lead to Huse database",
            "huse_response": huse_response
        })
        
    except Exception as e:
        print(f"Error in crm_to_huse_api: {str(e)}")
        return jsonify({"error": f"Internal server error: {str(e)}"}), 500
    
@app.route('/send_huse_credentials_email/<int:employee_id>', methods=['POST'])
def send_huse_credentials_email_route(employee_id):
    """
    Send Huse credentials email to a specific employee
    ---
    tags:
      - employees
    parameters:
      - name: huse-api-key
        in: header
        type: string
        required: true
        description: API key for authentication
      - name: employee_id
        in: path
        type: integer
        required: true
        description: The unique identifier of the employee
    responses:
      200:
        description: Employee successfully registered, credentials emailed, and account activated
        schema:
          type: object
          properties:
            success:
              type: boolean
              example: true
            message:
              type: string
              example: "Employee successfully registered, credentials emailed, and account activated"
            details:
              type: object
              properties:
                employee_name:
                  type: string
                  example: "John Doe"
                email_address:
                  type: string
                  example: "john@example.com"
                username:
                  type: string
                  example: "johndoe"
                password:
                  type: string
                  example: "[REDACTED]"
                security_question:
                  type: string
                  example: "What is your favorite color?"
                security_answer:
                  type: string
                  example: "[REDACTED]"
                employee_id:
                  type: integer
                  example: 123
                huse_user_id:
                  type: integer
                  example: 456
                email_sent:
                  type: boolean
                  example: true
                status_updated:
                  type: boolean
                  example: true
                status_message:
                  type: string
                  example: "Account activated successfully"
      400:
        description: Bad request - invalid employee ID or registration failure
        schema:
          type: object
          properties:
            success:
              type: boolean
              example: false
            message:
              type: string
              example: "Invalid employee ID"
            error:
              type: string
              example: "INVALID_INPUT"
      401:
        description: Unauthorized - invalid or missing API key
        schema:
          type: object
          properties:
            error:
              type: string
              example: "Unauthorized"
      500:
        description: Internal server error
        schema:
          type: object
          properties:
            success:
              type: boolean
              example: false
            message:
              type: string
              example: "Internal server error: ..."
            error:
              type: string
              example: "INTERNAL_ERROR"
    """
    try:
        # Check API key authentication
        api_key = request.headers.get("huse-api-key")
        print("Api key from headers: ", api_key)
        print("Api key from env: ", API_KEY)
        if api_key != API_KEY:
            return jsonify({"error": "Unauthorized"}), 401
        
        # Basic input validation
        if not employee_id or employee_id <= 0:
            return jsonify({
                "success": False,
                "message": "Invalid employee ID",
                "error": "INVALID_INPUT"
            }), 400
        
        # Call the email function
        result = send_employee_credentials_email(employee_id)
        
        # Return the result as JSON
        if result and result.get('success'):
            return jsonify(result), 200
        else:
            return jsonify(result), 400
            
    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"Internal server error: {str(e)}",
            "error": "INTERNAL_ERROR"
        }), 500
    
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5001)