import random
from faker import Faker
from sqlite3 import IntegrityError

from connection import create_connection, database
from default_data import (groups,
                          subjects,
                          faker_func,
                          groups_filling,
                          subject_lecturers,
                          grade_table_filling)


def table_creating(connection, sql_query):
    """ table creating function """
    cursor = connection.cursor()

    cursor.execute(sql_query)
    connection.commit()


students_table_query = """
    CREATE TABLE students(
    id INTEGER PRIMARY KEY,
    name VARCHAR(30)
    );
    """

groups_table_query = """
    CREATE TABLE groups(
    id INTEGER PRIMARY KEY,
    student_name VARCHAR(30),
    group_name VARCHAR(30),
    FOREIGN KEY (id) REFERENCES students(id)
    );
    """

lecturers_table_query = """
    CREATE TABLE lecturers(
    id INTEGER PRIMARY KEY,
    name VARCHAR(30),
    subject VARCHAR(10)
    );
    """

subjects_table_query = """
    CREATE TABLE subjects(
    id INTEGER PRIMARY KEY,
    subject VARCHAR(10),
    lecturer_name VARCHAR(30),
    FOREIGN KEY (lecturer_name) REFERENCES lecturers(name)
    );
    """

grades_table_query = """
    CREATE TABLE grades(
    student_name VARCHAR(30),
    group_name VARCHAR(30),
    subject VARCHAR(10),
    grade INTEGER,
    date DATE,
    FOREIGN KEY (student_name) REFERENCES students(name),
    FOREIGN KEY (group_name) REFERENCES groups(group_name),
    FOREIGN KEY (subject) REFERENCES subjects(subject),
    PRIMARY KEY (student_name, subject, date)
    );
    """


tables_drop = [
    'DROP TABLE IF EXISTS students;',
    'DROP TABLE IF EXISTS groups;',
    'DROP TABLE IF EXISTS lecturers;',
    'DROP TABLE IF EXISTS subjects;',
    'DROP TABLE IF EXISTS grades;'
]

queries = [
    students_table_query,
    groups_table_query,
    lecturers_table_query,
    subjects_table_query,
    grades_table_query
]


if __name__ == "__main__":
    Faker.seed(1)
    students = faker_func(random.randint(35, 50))
    lecturers = faker_func(5)
    groups_filling(students)
    subject_lecturers(lecturers)

    try:
        with create_connection(database) as conn:
            [table_creating(conn, i) for i in tables_drop]
            [table_creating(conn, i) for i in queries]

            # "groups" table filling in DB
            for group_name, students_list in groups.items():
                with conn:
                    cursor = conn.cursor()
                    for student in students_list:
                        insert_group_query = f"INSERT INTO groups (student_name, group_name) VALUES (?, ?)"
                        cursor.execute(insert_group_query, (student, group_name))

            # "students" table filling in DB
            for group_name, students_list in groups.items():
                with conn:
                    cursor = conn.cursor()
                    for student in students_list:
                        insert_student_query = f"INSERT INTO students (name) VALUES (?)"
                        cursor.execute(insert_student_query, (student,))

            # "lecturers" table filling in DB
            for subject, lecturer in subjects.items():
                with conn:
                    cursor = conn.cursor()
                    insert_lecturer_query = f"INSERT INTO lecturers (name, subject) VALUES (?, ?)"
                    cursor.execute(insert_lecturer_query, (lecturer, subject))

            # "subjects" table filling in DB
            for subject, lecturer in subjects.items():
                with conn:
                    cursor = conn.cursor()
                    cursor.execute(f"SELECT id FROM lecturers WHERE name=?", (lecturer,))
                    lecturer_id = cursor.fetchone()[0]
                    insert_subject_query = f"INSERT INTO subjects (subject, lecturer_name) VALUES (?, ?)"
                    cursor.execute(insert_subject_query, (subject, lecturer))

            # "grades" table filling in DB
            grades_data = grade_table_filling()
            for student, subjects in grades_data.items():
                with conn:
                    cursor = conn.cursor()
                    for subject, data in subjects.items():
                        cursor.execute(f"SELECT group_name FROM groups WHERE student_name=?", (student,))
                        group_name = cursor.fetchone()[0]
                        cursor.execute(f"SELECT id FROM students WHERE name=?", (student,))
                        student_id = cursor.fetchone()[0]
                        for grade, date in zip(data['grades'], data['date']):
                            insert_query = "INSERT INTO grades (student_name, group_name, subject, grade, date) VALUES (?, ?, ?, ?, ?)"
                            cursor.execute(insert_query, (student, group_name, subject, grade, date))

            conn.commit()

    except IntegrityError:
        pass

