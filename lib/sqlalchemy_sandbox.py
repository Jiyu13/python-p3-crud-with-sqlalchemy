#!/usr/bin/env python3

from datetime import datetime

from sqlalchemy import (create_engine, desc, func,
    CheckConstraint, PrimaryKeyConstraint, UniqueConstraint,
    Index, Column, DateTime, Integer, String)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class Student(Base):
    __tablename__ = 'students'

    # speed up lookups on certain column values
    Index("index_name", "name")

    id = Column(Integer(), primary_key=True)
    name = Column(String())
    email = Column(String(55))
    grade = Column(Integer())
    birthday = Column(DateTime())
    enrolled_date = Column(DateTime(), default=datetime.now())

    # print the instance
    def __repr__(self):
        return f"Student {self.id}:" \
                + f"{self.name, }" \
                + f"Grade {self.grade}"
    
    # my_student = Student(...)
    # print(my_student)
    # => Student 1: Joseph Smith, Grade 4


if __name__ == '__main__':
    # 1. use a sqlite db in memory instead of a students.db file
    engine = create_engine('sqlite:///:memory:')
    Base.metadata.create_all(engine)

    # 2. use engine to configure a "Session" class
    Session = sessionmaker(bind=engine)

    # 3. use "Session" class to create "session" object
    session = Session()

    # 4. =====================create an record in db=============================
    albert_einstein = Student(
        name="Albert Einstein",
        email="albert.einstein@zurich.edu",
        grade=6,
        birthday=datetime(
            year=1879,
            month=3,
            day=14
        ),
    )

    # create session, student objects
    # generate a statement to include in the session's transaction
    # commit() executes all statements in the transaction, save any changes to db, update your Student object with an id
    # session.add(albert_einstein)
    # session.commit()
    # print(f"New student ID is {albert_einstein.id}.")
    # python lib/sqlalchemy_sandbox.p
    # New student ID is 1.

    print("line 70: ", albert_einstein)
    # line 81:  Student None:('Albert Einstein',)Grade 6

    alan_turing = Student(
        name="Alan Turing",
        email="alan.turing@sherborne.edu",
        grade=11,
        birthday=datetime(
            year=1912,
            month=6,
            day=23
        ),
    )

    

    # # create session, student objects
    session.bulk_save_objects([albert_einstein, alan_turing])
    session.commit()
    print(f"New student ID is {albert_einstein.id}.")
    print(f"New student ID is {alan_turing.id}.")
    # python lib/sqlalchemy_sandbox.p
    # New student ID is None.
    # New student ID is None.   
    # ==========================================================================

    # 5. ================== Read Records ======================================
    students = session.query(Student)
    # students = session.query(Student).all()
    print([student for student in students])
    # python lib/sqlalchemy_sandbox.p
    # [Student 1:('Albert Einstein',)Grade 6, Student 2:('Alan Turing',)Grade 11]
    # ==========================================================================

    # 6. ============= Select Only Certain Columns ============================
    names = session.query(Student.name).all()    print(names)
    # [('Albert Einstein',), ('Alan Turing',)]
    # =========================================================================

    # 7. ============== Ordering ==============================================
    students_by_name = session.query(Student.name).order_by(Student.name).all()
    print(students_by_name)
    # [('Alan Turing',), ('Albert Einstein',)]

    students_by_grade_desc = session.query(Student.name, Student.grade).order_by(
        desc(Student.grade)).all()
    print(students_by_grade_desc)
    # [('Alan Turing', 11), ('Albert Einstein', 6)]
    # =========================================================================

    # 8. ============== Limiting ==============================================
    oldest_student = session.query(Student.name, Student.birthday).order_by(
        desc(Student.grade)).limit(1).all()

    # oldest_student = session.query(
    #         Student.name, Student.birthday).order_by(
    #         desc(Student.grade)).first()

    print(oldest_student)
    # [('Alan Turing', datetime.datetime(1912, 6, 23, 0, 0))]

    # =========================================================================

    # 9. ====== func - access SQL operation functuions ===========
    student_count = session.query(func.count(Student.id)).first()
    print(student_count)
    # (2,)
    # =========================================================================

    # 10. ================ Filtering  =========================================
    records = session.query(Student).filter(
        Student.name.like('%Alan%'), Student.grade == 11).all()
    for record in records:
       print(record.name)
    # Alan Turing
    # =========================================================================

    # 11. ================ updating data  =========================================
    # method 1 => for loop
    for student in session.query(Student):
        student.grade += 1
    session.commit()
    print([(student.name, student.grade) for student in session.query(Student)])
    # [('Albert Einstein', 7), ('Alan Turing', 12)]

    # method 2 => update()
    session.query(Student).update({Student.grade: Student.grade + 1})
    # session.commit()
    print([(student.name, student.grade) for student in session.query(Student)])
    # [('Albert Einstein', 8), ('Alan Turing', 13)]
    # =========================================================================

    # 13. ================ deleting data  =====================================
    query = session.query(Student).filter(Student.name == "Albert Einstein")
    # method 1:
    # retrieve first matching record as object
    albert_einstein = query.first()
    # delete record
    session.delete(albert_einstein)
    session.commit()

    # try to retrieve deleted record
    albert_einstein = query.first()
    print(albert_einstein)
    # None

    # method 2: if don't have a single object ready for deletion but know the criteria for deletiong
    # call delete() from query instead
    query.delete()
    albert_einstein = query.first()
    print(albert_einstein)
    # None
    # =========================================================================

# run chmod +x lib/sqlalchemy_sandbox.py to make this file executable