from sqlalchemy.orm import Session

import models, schemas


def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def get_all_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


def create_user(db: Session, user: schemas.UserCreate):
    fake_hashed_password = user.password + "notreallyhashed"
    db_user = models.User(email=user.email, hashed_password=fake_hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_items(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Item).offset(skip).limit(limit).all()


def create_message(db: Session, message: schemas.MessageCreate, user_id: int):
    db_item = models.Message(content=message, owner_id=user_id)### тут всё не так
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


def get_messages_for_user(db: Session, user_id: int):
    return db.query(models.Message).filter(models.User.id == user_id).first()


def authenticate_user(db: Session):
    pass


def delete_user(db: Session):
    pass