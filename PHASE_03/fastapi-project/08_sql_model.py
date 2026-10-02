from typing import Annotated
from fastapi import FastAPI, Depends, HTTPException, status
from sqlmodel import SQLModel, Field, Session, create_engine, select

app = FastAPI()

class Student(SQLModel, table=True): # tells python to actually create a SQL table on the disk
    id: int | None = Field(default=None, primary_key=True) # be default it is None cuz user will not pass a key, the model will create a key itself when creating a Student
    name: str = Field(index=True)
    age: int = Field(index=True)

sqlite_filename = "database.db" # the actual db file where our data will be stored
sqlite_url = f"sqlite:///{sqlite_filename}" # the sql db url

# engine is like a telephone line that we set up only once for our entire app
engine = create_engine(url=sqlite_url, connect_args={"check_same_thread": False}) 

def create_db_and_tables(): # the actual function that creates the database and tables for us
    SQLModel.metadata.create_all(engine)

# session is like a telephone call on that engine so each user request is a separate session
def get_session():
    with Session(engine) as session: # the with block opens a session and closes it itself
        yield session

@app.on_event("startup")
def on_startup(): # calling the above create_db_and_tables() function on this endpoint
    create_db_and_tables()

# we could also pass this session in the below post endpoint as session: SessionDep
# SessionDep = Annotated[Session, Depends(get_session)]

@app.post("/students/")
def create_student(student: Student, session: Session = Depends(get_session)): # as multiple requests can hit this API at once, Depends(get_session) creates a separate session for eah request so that they two requests don't clash
    
    try:
        session.add(student) # just adds the student to like a notepad
        session.commit() # saves the data to our db. the SQL commands are run internally. the id is generated 
        session.refresh(student) # makes sure the id is present according to the Student model we made
        session.close() # closes the connectin
        return student
    except:
        raise HTTPException(detail="Couldn't create student!")

@app.get("/all_students")
def read_all_students(session: Session = Depends(get_session)) -> list[Student]:
    students = session.exec(select(Student)).all()
    return students

@app.get("/students/{student_id}")
def read_student(student_id: int, session: Session = Depends(get_session)):
    student = session.get(Student, student_id)
    if not student:
        raise HTTPException(detail="Student not found!")
    return student

@app.delete("/students/{student_id}")
def delete_student(student_id: int, session: Session = Depends(get_session)):
    student = session.get(Student, student_id)
    if not student:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Student not found")
    
    session.delete(student)
    session.commit()
    return {"Ok": True, "message":"Student deleted"}