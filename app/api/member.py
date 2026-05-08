from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.deps import get_db
from app.models.member import Member
from app.schemas.member import MemberCreate, MemberResponse

router = APIRouter(prefix="/members", tags=["Members"])


@router.post("/", response_model=MemberResponse)
def create_member(member: MemberCreate, db: Session = Depends(get_db)):
    new_member = Member(
        user_name=member.user_name,
        email=member.email
    )
    db.add(new_member)
    db.commit()
    db.refresh(new_member)
    return new_member


@router.get("/", response_model=list[MemberResponse])
def get_members(db: Session = Depends(get_db)):
    members = db.query(Member).all()
    return members
