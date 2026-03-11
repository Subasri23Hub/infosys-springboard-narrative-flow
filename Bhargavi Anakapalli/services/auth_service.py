import bcrypt
from sqlalchemy.orm import Session
from database.models import User

def hash_password(password: str) -> str:
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')

def verify_password(plain_password: str, hashed_password: str) -> bool:
    try:
        return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))
    except Exception:
        # Fallback if the user has an old plaintext or SHA-256 hash
        # Since we migrated from sha256 in json to bcrypt, older accounts might fail
        # This will be handled if necessary, but bcrypt checkpw catches mismatched formats
        return False

def get_user_by_username(db: Session, username: str) -> User | None:
    return db.query(User).filter(User.username == username).first()

def get_user_by_id(db: Session, user_id: int) -> User | None:
    return db.query(User).filter(User.id == user_id).first()

def create_user(db: Session, username: str, password_plain: str, email: str = None, bio: str = "") -> User:
    hashed = hash_password(password_plain)
    db_user = User(username=username, password_hash=hashed, email=email, bio=bio)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
