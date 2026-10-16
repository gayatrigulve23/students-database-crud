from datetime import date
from pydantic import BaseModel, ConfigDict, EmailStr, Field, model_validator


class StudentBase(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    date_of_birth: date
    email: EmailStr | None = None
    phone: str | None = Field(default=None, min_length=7, max_length=20)
    course: str | None = Field(default=None, max_length=100)
    address: str | None = Field(default=None, max_length=250)
    enrollment_date: date | None = None

    @model_validator(mode="after")
    def require_contact_information(self):
        if not self.email and not self.phone:
            raise ValueError("Provide at least one contact method: email or phone.")
        return self


class StudentCreate(StudentBase):
    pass


class StudentUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=100)
    date_of_birth: date | None = None
    email: EmailStr | None = None
    phone: str | None = Field(default=None, min_length=7, max_length=20)
    course: str | None = Field(default=None, max_length=100)
    address: str | None = Field(default=None, max_length=250)
    enrollment_date: date | None = None

    @model_validator(mode="after")
    def prevent_empty_update(self):
        if not self.model_fields_set:
            raise ValueError("Provide at least one field to update.")
        return self


class StudentResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    date_of_birth: date
    email: EmailStr | None
    phone: str | None
    course: str | None
    address: str | None
    enrollment_date: date | None
