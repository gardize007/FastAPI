
from fastapi import HTTPException
from sqlalchemy.orm import Session
from db.model import DbRating, DbTransaction
from schemas import RatingCreate

def create_rating(db: Session, rating: RatingCreate, current_user: int):
    transaction = db.query(DbTransaction).filter(DbTransaction.id == rating.transaction_id).first()
    if not transaction:
        raise HTTPException(status_code=404, detail="Transaction not found")

    if not transaction.completed:
        raise HTTPException(status_code=400, detail="Transaction not completed")

    if current_user != transaction.buyer_id and current_user != transaction.seller_id:
        raise HTTPException(status_code=403, detail="User not involved in this transaction")

    # Prevent duplicate rating by same user on same transaction
    existing_rating = db.query(DbRating).filter(
        DbRating.transaction_id == rating.transaction_id,
        DbRating.rater_id == current_user
    ).first()
    if existing_rating:
        raise HTTPException(status_code=400, detail="Rating already exists for this transaction by this user")  
        

    # Determine who is being rated
    if current_user == transaction.buyer_id:
        ratee_id = transaction.seller_id
        rater_id = transaction.buyer_id
    else:
        ratee_id = transaction.buyer_id
        rater_id = transaction.seller_id

    new_rating = DbRating(
        transaction_id=rating.transaction_id,
        rater_id=rater_id,
        ratee_id=ratee_id,
        score=rating.score,
        comment=rating.comment
    )
    db.add(new_rating)
    db.commit()
    db.refresh(new_rating)
    return new_rating


def get_ratings_for_user(db: Session, user_id: int):
    return db.query(DbRating).filter(DbRating.ratee_id == user_id).all()