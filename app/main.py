from contextlib import asynccontextmanager
from datetime import date
from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, Query, Response, status
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from .database import Base, engine, get_db
from .models import Student
from .schemas import StudentCreate, StudentResponse, StudentUpdate


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Create the SQLite table on first startup.
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(
    title="Students Database CRUD API",
    description=(
        "An internship project demonstrating student record management "
        "with FastAPI and SQLite. Use only dummy student data."
    ),
    version="1.0.0",
    lifespan=lifespan,
)


@app.get("/", tags=["General"])
def home():
    return {
        "message": "Students Database CRUD API is running.",
        "docs": "/docs",
        "students_endpoint": "/students",
    }


@app.post(
    "/students",
    response_model=StudentResponse,
    status_code=status.HTTP_201_CREATED,
    tags=["Students"],
    summary="Create a student",
)
def create_student(
    student_data: StudentCreate,
    db: Annotated[Session, Depends(get_db)],
):
    student = Student(**student_data.model_dump())
    db.add(student)
    try:
        db.commit()
        db.refresh(student)
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="A student with this email already exists.",
        )
    return student


@app.get(
    "/students",
    response_model=list[StudentResponse],
    tags=["Students"],
    summary="List and filter students",
)
def list_students(
    db: Annotated[Session, Depends(get_db)],
    name: str | None = Query(default=None, description="Filter by part of a name"),
    course: str | None = Query(default=None, description="Filter by course"),
    born_after: date | None = Query(default=None, description="Date of birth after this date"),
):
    statement = select(Student).order_by(Student.id)
    if name:
        statement = statement.where(Student.name.ilike(f"%{name}%"))
    if course:
        statement = statement.where(Student.course.ilike(f"%{course}%"))
    if born_after:
        statement = statement.where(Student.date_of_birth > born_after)
    return db.scalars(statement).all()


@app.get(
    "/students/{student_id}",
    response_model=StudentResponse,
    tags=["Students"],
    summary="Get one student",
)
def get_student(student_id: int, db: Annotated[Session, Depends(get_db)]):
    student = db.get(Student, student_id)
    if student is None:
        raise HTTPException(status_code=404, detail="Student not found.")
    return student


@app.put(
    "/students/{student_id}",
    response_model=StudentResponse,
    tags=["Students"],
    summary="Replace student details",
)
def update_student(
    student_id: int,
    student_data: StudentCreate,
    db: Annotated[Session, Depends(get_db)],
):
    student = db.get(Student, student_id)
    if student is None:
        raise HTTPException(status_code=404, detail="Student not found.")
    for field, value in student_data.model_dump().items():
        setattr(student, field, value)
    try:
        db.commit()
        db.refresh(student)
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="A student with this email already exists.",
        )
    return student


@app.patch(
    "/students/{student_id}",
    response_model=StudentResponse,
    tags=["Students"],
    summary="Partially update student details",
)
def patch_student(
    student_id: int,
    student_data: StudentUpdate,
    db: Annotated[Session, Depends(get_db)],
):
    student = db.get(Student, student_id)
    if student is None:
        raise HTTPException(status_code=404, detail="Student not found.")

    changes = student_data.model_dump(exclude_unset=True)
    if not changes:
        raise HTTPException(status_code=422, detail="Provide at least one field to update.")

    for field, value in changes.items():
        setattr(student, field, value)

    # If both contact methods are explicitly removed, reject the update.
    if not student.email and not student.phone:
        raise HTTPException(
            status_code=422,
            detail="A student must have at least one contact method: email or phone.",
        )

    try:
        db.commit()
        db.refresh(student)
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="A student with this email already exists.",
        )
    return student


@app.delete(
    "/students/{student_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    tags=["Students"],
    summary="Delete a student",
)
def delete_student(student_id: int, db: Annotated[Session, Depends(get_db)]):
    student = db.get(Student, student_id)
    if student is None:
        raise HTTPException(status_code=404, detail="Student not found.")
    db.delete(student)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
