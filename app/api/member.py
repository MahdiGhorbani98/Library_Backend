from fastapi import APIRouter, Depends, Path
from sqlalchemy.orm import Session

from app.core.deps import get_db
from app.models.member import Member
from app.schemas import member
from app.schemas.member import MemberCreate, MemberResponse, MemberUpdate

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
    if member is not None:
        return member


@member_router.post("/", response_model=MemberResponse)
def create_member(member: MemberCreate, db: Session = Depends(get_db)):
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


@member_router.put('/{member_id}')
def update_memeber(member_update: MemberUpdate, member_id: int = Path(gt=0),  db: Session = Depends(get_db)):
    member = db.query(Member).filter(Member.id == member_id).first()
    member.user_name = member_update.user_name
    member.email = member_update.email
    member.is_borrowing = member_update.is_borrowing
    member.status = member_update.status
    db.add(member)
    db.commit()


@member_router.delete('/{member_id}')
def delete_member(member_id: int = Path(gt=0), db: Session = Depends(get_db)):
    member = db.query(Member).filter(Member.id == member_id).first()
    db.delete(member)
    db.commit()

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
