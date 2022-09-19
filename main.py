from sqlite3 import Error
from connection import create_connection
from random import randint, choice
from requests import (get_students_with_max_avg_score, get_student_with_max_avg_score_by_subject,
                      get_avg_score_by_subject_in_class, get_avg_score_in_class, get_subjects_by_mentor,
                      get_students_by_class, get_marks_by_class_and_subject,
                      get_marks_by_class_and_subject_on_last_subject, get_subjects_by_student,
                      get_subjects_by_student_and_mentor, get_avg_score_by_student_and_mentor, get_avg_score_by_mentor)
from faker import Faker
fake = Faker()


def create_table():
    try:
        with create_connection() as conn:
            if conn is not None:
                c = conn.cursor()
                c.execute('''CREATE TABLE IF NOT EXISTS class (
                         id SERIAL PRIMARY KEY,
                         class_name VARCHAR(30) NOT NULL
                        )''')

                c.execute('''CREATE TABLE IF NOT EXISTS student (
                         id SERIAL PRIMARY KEY,
                         name VARCHAR(30) NOT NULL,
                         class_id INTEGER REFERENCES class(id)
                        )''')

                c.execute('''CREATE TABLE IF NOT EXISTS mentor (
                         id SERIAL PRIMARY KEY,
                         name VARCHAR(30) NOT NULL
                        )''')

                c.execute('''CREATE TABLE IF NOT EXISTS subject (
                         id SERIAL PRIMARY KEY,
                         subject_name VARCHAR(30) NOT NULL,
                         mentor_id INTEGER REFERENCES mentor(id)
                        )''')

                c.execute('''CREATE TABLE IF NOT EXISTS mark (
                         id SERIAL PRIMARY KEY,
                         mark INTEGER NOT NULL,
                         date_mark DATE NOT NULL,
                         student_id INTEGER REFERENCES student(id),
                         subject_id INTEGER REFERENCES subject(id)
                        )''')
    except Error as e:
        print(e)


def insert_data():
    try:
        with create_connection() as conn:
            if conn is not None:
                c = conn.cursor()
                for i in range(3):
                    c.execute(
                        "INSERT INTO class (class_name) VALUES (%s)",
                        (fake.bothify(text='Class: ??-##', letters='ABCDE'),)
                    )

                c.execute("SELECT id FROM class")
                class_ids = c.fetchall()
                conn.commit()

                for i in range(30):
                    c.execute(
                        "INSERT INTO student (name, class_id) VALUES (%s, %s)",
                        (fake.name(), choice(class_ids))
                    )

                c.execute("SELECT id FROM student")
                student_ids = c.fetchall()
                conn.commit()

                for i in range(3):
                    c.execute(
                        "INSERT INTO mentor (name) VALUES (%s)",
                        (fake.name(),)
                    )

                c.execute("SELECT id FROM mentor")
                mentor_ids = c.fetchall()
                conn.commit()

                for subject in ['Arithmetic', 'Algebra', 'Geometry', 'Topology', 'Probability theory']:
                    c.execute(
                        "INSERT INTO subject (subject_name, mentor_id) VALUES (%s, %s)",
                        (subject, choice(mentor_ids))
                    )

                c.execute("SELECT id FROM subject")
                subject_ids = c.fetchall()
                conn.commit()

                for student in student_ids:
                    for subject in subject_ids:
                        for i in range(20):
                            c.execute(
                                "INSERT INTO mark (mark, date_mark, student_id, subject_id) VALUES (%s, %s, %s, %s)",
                                (randint(1, 12), fake.date_this_year(), student[0], subject[0])
                            )
    except Error as e:
        print(e)


if __name__ == "__main__":
    create_table()
    insert_data()

    # print(get_students_with_max_avg_score())
    # print(get_student_with_max_avg_score_by_subject(1))
    # print(get_avg_score_by_subject_in_class(1, 1))
    # print(get_avg_score_in_class())
    # print(get_subjects_by_mentor(1))
    # print(get_students_by_class(1))
    # print(get_marks_by_class_and_subject(1, 1))
    # print(get_marks_by_class_and_subject_on_last_subject(1, 1))
    # print(get_subjects_by_student(1))
    # print(get_subjects_by_student_and_mentor(1, 1))
    # print(get_avg_score_by_student_and_mentor(1, 1))
    # print(get_avg_score_by_mentor(1))
