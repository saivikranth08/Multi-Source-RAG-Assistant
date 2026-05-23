from backend.database.models import SessionLocal, ChatMessage
import uuid
from datetime import datetime

class DatabaseMemory:
    def __init__(self, session_id: str):
        self.session_id = session_id
        self.db = SessionLocal()
    
    def save_context(self, input_dict, output_dict):
        message = ChatMessage(
            id=str(uuid.uuid4()),
            session_id=self.session_id,
            user_query=input_dict["input"],
            ai_answer=output_dict["output"],
            created_at=datetime.utcnow()
        )
        self.db.add(message)
        self.db.commit()
    
    def load_memory_variables(self, _):
        messages = self.db.query(ChatMessage).filter(
            ChatMessage.session_id == self.session_id
        ).order_by(ChatMessage.created_at).all()
        
        history = ""
        for msg in messages:
            history += f"Human: {msg.user_query}\nAI: {msg.ai_answer}\n\n"
        
        return {"history": history}
    
    def clear(self):
        self.db.query(ChatMessage).filter(
            ChatMessage.session_id == self.session_id
        ).delete()
        self.db.commit()
