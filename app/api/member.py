from fastapi import APIRouter, Depends, Path
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.orm import Session
import logging

from app.core.deps import get_db
from app.core.exceptions import EntityNotFound, DuplicateResource, BadRequestError, InternalServerError
from app.models.member import Member
from app.schemas import member
from app.schemas.member import MemberCreate, MemberResponse, MemberUpdate

logger = logging.getLogger(__name__)


# Create a router for member endpoints with /members prefix
member_router = APIRouter(prefix="/members", tags=["Members"])


@member_router.get("/", response_model=list[MemberResponse])
def get_members(db: Session = Depends(get_db)):
    # ? db.query(Member) creates a SQLAlchemy query object.
    # ? Quick rule: use .all() when you want all rows from a query.
    members = db.query(Member).all()
    return members


@member_router.get('/{member_id}', response_model=MemberResponse)
def get_member(db: Session = Depends(get_db), member_id: int = Path(gt=0)):
    member = db.query(Member).filter(Member.id == member_id).first()
    if not member:
        raise EntityNotFound("Member", member_id)
    return member


@member_router.post("/", response_model=MemberResponse)
def create_member(member: MemberCreate, db: Session = Depends(get_db)):
    if db.query(Member).filter((Member.email == member.email) | (Member.user_name == member.user_name)).first():
        raise DuplicateResource("Email/User", member.email or member.user_name)

    try:
        # Create a new Member instance with data from the request
        new_member = Member(
            user_name=member.user_name,
            email=member.email
        )
        # Add the new member object to the database session
        db.add(new_member)
        # Commit the transaction to save the member to the database
        db.commit()
        # Refresh the object to populate it with database-generated fields (like ID)
        db.refresh(new_member)
        # Return the newly created member
        return new_member
    except IntegrityError:
        db.rollback()
        logger.exception("Integrity error creating member")
        raise DuplicateResource("Email/User", "conflict")
    except SQLAlchemyError:
        db.rollback()
        logger.exception("Database error creating member")
        raise InternalServerError("Unable to create member")


@member_router.put('/{member_id}')
def update_memeber(member_update: MemberUpdate, member_id: int = Path(gt=0),  db: Session = Depends(get_db)):
    member = db.query(Member).filter(Member.id == member_id).first()
    if not member:
        raise EntityNotFound("Member", member_id)

    existing = db.query(Member).filter(
        ((Member.email == member_update.email) | (Member.user_name == member_update.user_name)) &
        (Member.id != member_id)
    ).first()
    if existing:
        raise DuplicateResource(
            "Email/User", member_update.email or member_update.user_name)

    try:
        member.user_name = member_update.user_name
        member.email = member_update.email
        member.is_borrowing = member_update.is_borrowing
        member.status = member_update.status
        db.add(member)
        db.commit()
        db.refresh(member)
        return member
    except IntegrityError:
        db.rollback()
        logger.exception("Integrity error updating member %s", member_id)
        raise DuplicateResource("Email/User", "conflict")
    except SQLAlchemyError:
        db.rollback()
        logger.exception("Database error updating member %s", member_id)
        raise InternalServerError("Unable to update member")


@member_router.delete('/{member_id}')
def delete_member(member_id: int = Path(gt=0), db: Session = Depends(get_db)):
    member = db.query(Member).filter(Member.id == member_id).first()
    if not member:
        raise EntityNotFound("Member", member_id)

    try:
        db.delete(member)
        db.commit()
        return {"detail": "Member deleted"}
    except SQLAlchemyError:
        db.rollback()
        logger.exception("Database error deleting member %s", member_id)
        raise InternalServerError("Unable to delete member")

    # Soft delete member (optional)

    # ! Handle authentication
    # ! follow a good pattern for error handling and validation in the future (reuse it across all endpoints)
    # ! follow a good pattern for status code (reuse it across all endpoints)

    # * why we don't use async here?
    # Recommendation:
    # If traffic is low/medium: Keep synchronous(easier, less complex)
    # If you want async: Switch your database to async driver + update all endpoints

    # * best sorting in CRUD operations:
    # GET all (read list)
    # GET specific (read detail)
    # POST (create)
    # PUT (update)
    # DELETE (remove)
