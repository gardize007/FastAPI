from sqlalchemy.orm.session import Session
from db.database import get_db
from db.model import DbCategory
from schemas import CategoryBase


def create_category(db: Session, request: CategoryBase):
    new_category = DbCategory(title=request.title)
    db.add(new_category)
    db.commit()
    db.refresh(new_category)
    return new_category


def get_all(db: Session):
    return db.query(DbCategory).all()
