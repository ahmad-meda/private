from services.employee_message_service import LeadMessageHistoryService

class LeadMessageHistoryProxy:
    @staticmethod
    def get_message_history(contact_number):
        from app import app, db
        with app.app_context():
            return LeadMessageHistoryService.get_message_history(
                db.session, contact_number
            )

    @staticmethod
    def save_message(contact_number, role, content):
        from app import app, db
        with app.app_context():
            return LeadMessageHistoryService.save_message(
                db.session, contact_number, role, content
            )

    @staticmethod
    def clear_message_history(contact_number):
        from app import app, db
        with app.app_context():
            return LeadMessageHistoryService.clear_message_history(
                db.session, contact_number
            )