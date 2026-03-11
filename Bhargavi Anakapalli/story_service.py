from sqlalchemy.orm import Session
from database.models import Story, StoryVersion

def create_story(db: Session, user_id: int, title: str, initial_content: str = "") -> Story:
    db_story = Story(user_id=user_id, title=title, content=initial_content)
    db.add(db_story)
    db.commit()
    db.refresh(db_story)
    return db_story

def get_stories_by_user(db: Session, user_id: int) -> list[Story]:
    return db.query(Story).filter(Story.user_id == user_id).order_by(Story.created_at.desc()).all()

def get_story_by_id(db: Session, story_id: int, user_id: int) -> Story | None:
    return db.query(Story).filter(Story.id == story_id, Story.user_id == user_id).first()

def update_story_content(db: Session, story_id: int, user_id: int, new_title: str, new_content: str) -> Story | None:
    story = get_story_by_id(db, story_id, user_id)
    if not story:
        return None
    
    story.title = new_title
    story.content = new_content
    db.commit()
    db.refresh(story)
    return story

def save_story_version(db: Session, story_id: int, content: str) -> StoryVersion:
    version = StoryVersion(story_id=story_id, content=content)
    db.add(version)
    db.commit()
    db.refresh(version)
    return version
