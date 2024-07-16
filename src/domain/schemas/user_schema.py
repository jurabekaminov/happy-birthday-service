from datetime import date, datetime

from pydantic import BaseModel, Field, field_validator, validate_email


class UserCreateSchema(BaseModel):
    name: str = Field(max_length=64)
    surname: str = Field(max_length=64)
    patronymic: str | None = Field(max_length=64)
    email: str = Field(max_length=64)
    password_text: str = Field(min_length=8, max_length=64)
    date_of_birth: date
    
    @field_validator("email")
    @classmethod
    def check_email(cls, email: str) -> str:
        try:
            _ = validate_email(email)
        except Exception as e:
            raise ValueError(e)
        return email


class UserReadSchema(BaseModel):
    id: int
    name: str
    surname: str
    patronymic: str | None
    email: str
    date_of_birth: date
    created_at: datetime
    updated_at: datetime
