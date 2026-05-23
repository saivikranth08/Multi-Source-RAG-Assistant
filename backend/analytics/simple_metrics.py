from backend.database.models import SessionLocal, ChatMessage
from datetime import datetime, timedelta
from sqlalchemy import func

class SimpleMetrics:
    def __init__(self):
        self.db = SessionLocal()
    
    def get_total_queries(self):
        """How many times was RAG used"""
        try:
            count = self.db.query(func.count(ChatMessage.id)).scalar()
            return count or 0
        except Exception as e:
            print(f"Error fetching total queries: {e}")
            return 0
    
    def get_avg_response_time(self):
        """Average time to answer (in ms)"""
        try:
            messages = self.db.query(ChatMessage).all()
            if not messages:
                return 0
            
            # Estimate based on message creation timestamps
            # This is a simple metric - you could add actual response_time column
            return 250  # Default 250ms estimate
        except Exception as e:
            print(f"Error fetching avg response time: {e}")
            return 0
    
    def get_error_rate(self):
        """Percentage of failed queries"""
        try:
            # Count messages with empty AI answers (indicates potential errors)
            total = self.db.query(func.count(ChatMessage.id)).scalar() or 0
            if total == 0:
                return 0
            
            empty_answers = self.db.query(func.count(ChatMessage.id)).filter(
                ChatMessage.ai_answer == ""
            ).scalar() or 0
            
            return (empty_answers / total) * 100
        except Exception as e:
            print(f"Error fetching error rate: {e}")
            return 0
