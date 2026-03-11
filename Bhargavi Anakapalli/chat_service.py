from sqlalchemy.orm import Session
from database.models import Chats

def save_chat(db: Session, story_id: int, role: str, message: str) -> Chats:
    chat = Chats(story_id=story_id, role=role, message=message)
    db.add(chat)
    db.commit()
    db.refresh(chat)
    return chat

def get_chat_history(db: Session, story_id: int) -> list[Chats]:
    return db.query(Chats).filter(Chats.story_id == story_id).order_by(Chats.timestamp.asc()).all()
