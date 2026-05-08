from datetime import datetime
from pydantic import BaseModel, ConfigDict, EmailStr


class MemberCreate(BaseModel):
    user_name: str
    email: EmailStr


class MemberUpdate(BaseModel):
    user_name: str | None = None
    email: EmailStr | None = None
    is_borrowing: bool | None = None
    status: str | None = None


class MemberResponse(BaseModel):
    id: int
    user_name: str
    email: EmailStr
    is_borrowing: bool
    status: str
    created_at: datetime
    updated_at: datetime | None = None

    model_config = ConfigDict(from_attributes=True)
