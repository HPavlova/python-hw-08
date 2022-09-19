from sqlite3 import Error
from connection import create_connection


def get_data(request, data_id=None):
    try:
        with create_connection() as conn:
            if conn is not None:
                c = conn.cursor()
                c.execute(request, data_id)
                return c.fetchall()
    except Error as e:
        print(e)


# 5 студентов с наибольшим средним баллом по всем предметам.
def get_students_with_max_avg_score():
    request = '''
            SELECT s.name, ROUND(AVG(m.mark), 2) AS avg_mark
            FROM mark m
            JOIN student s ON s.id = m.student_id
            GROUP BY s.id
            ORDER BY avg_mark desc
            LIMIT 5;
            '''
    return get_data(request)


# 1 студент с наивысшим средним баллом по одному предмету.
def get_student_with_max_avg_score_by_subject(subject_id):
    request = '''
            SELECT s2.subject_name, ROUND(AVG(m.mark), 2) AS avg_mark
            FROM mark m
            LEFT JOIN student s ON s.id = m.student_id
            LEFT JOIN subject s2 ON s2.id = m.subject_id
            WHERE s2.id = %s
            GROUP BY s2.id, s.id
            ORDER BY avg_mark desc
            LIMIT 1;
            '''
    return get_data(request, (subject_id,))


# средний балл в группе по одному предмету.
def get_avg_score_by_subject_in_class(class_id, subject_id):
    request = '''
            SELECT subject.subject_name, c.class_name, ROUND(AVG(m.mark), 2) AS avg_mark
            FROM mark m
            LEFT JOIN student s ON s.id = m.student_id
            LEFT JOIN subject ON subject.id = m.subject_id
            LEFT JOIN class c ON c.id = s.class_id
            WHERE c.id = %s AND subject_id = %s
            GROUP BY c.id, subject.id
            ORDER BY avg_mark desc
            '''
    return get_data(request, (class_id, subject_id))


# Средний балл в потоке.
def get_avg_score_in_class():
    request = '''
            SELECT ROUND(AVG(mark.mark), 2) AS avg_mark
            FROM mark 
            '''
    return get_data(request)


# Какие курсы читает преподаватель.
def get_subjects_by_mentor(mentor_id):
    request = '''
            SELECT name, s.subject_name
            FROM mentor
            LEFT JOIN subject s ON mentor.id = s.mentor_id
            WHERE mentor.id = %s
            '''
    return get_data(request, (mentor_id,))


# Список студентов в группе.
def get_students_by_class(class_id):
    request = '''
            SELECT s.name, c.class_name
            FROM student s
            LEFT JOIN class c ON s.class_id = c.id
            WHERE c.id = %s;
            '''
    return get_data(request, (class_id,))


# Оценки студентов в группе по предмету.
def get_marks_by_class_and_subject(student_id, class_id):
    request = '''
            SELECT s.name, m.mark, m.date_mark, c.class_name, s2.subject_name
            FROM mark m
            LEFT JOIN student s ON s.id = m.student_id
            LEFT JOIN class c ON c.id = s.class_id
            LEFT JOIN subject s2 ON s2.id = m.subject_id
            WHERE student_id = %s AND subject_id = %s
            '''
    return get_data(request, (student_id, class_id))


# Оценки студентов в группе по предмету на последнем занятии.
def get_marks_by_class_and_subject_on_last_subject(student_id, subject_id):
    request = '''
            SELECT s.name, m.mark, m.date_mark, c.class_name, s2.subject_name
            FROM mark m
            LEFT JOIN student s ON s.id = m.student_id
            LEFT JOIN class c ON c.id = s.class_id
            LEFT JOIN subject s2 ON s2.id = m.subject_id
            WHERE student_id = %s AND subject_id = %s
            ORDER BY date_mark DESC
            LIMIT 1
            '''
    return get_data(request, (student_id, subject_id))


# Список курсов, которые посещает студент.
def get_subjects_by_student(student_id):
    request = '''
            SELECT DISTINCT s.name, s2.subject_name
            FROM mark m
            LEFT JOIN student s ON s.id = m.student_id
            LEFT JOIN subject s2 ON s2.id = m.subject_id
            WHERE s.id = %s
            '''
    return get_data(request, (student_id,))


# Список курсов, которые студенту читает преподаватель.
def get_subjects_by_student_and_mentor(student_id, mentor_id):
    request = '''
            SELECT DISTINCT s.name, s2.subject_name, m2.name
            FROM mark m
            LEFT JOIN student s ON s.id = m.student_id
            LEFT JOIN subject s2 ON s2.id = m.subject_id
            LEFT JOIN mentor m2 ON m2.id = s2.mentor_id
            WHERE s.id = %s AND m2.id = %s
            '''
    return get_data(request, (student_id, mentor_id))


# Средний балл, который преподаватель ставит студенту.
def get_avg_score_by_student_and_mentor(student_id, mentor_id):
    request = '''
            SELECT DISTINCT s.name, m2.name, ROUND(AVG(m.mark), 2) AS avg_mark
            FROM mark m
            LEFT JOIN student s ON s.id = m.student_id
            LEFT JOIN subject s2 ON s2.id = m.subject_id
            LEFT JOIN mentor m2 ON m2.id = s2.mentor_id
            WHERE s.id = %s AND m2.id = %s
            GROUP BY s.name, m2.name;
            '''
    return get_data(request, (student_id, mentor_id))


# Средний балл, который ставит преподаватель.
def get_avg_score_by_mentor(mentor_id):
    request = '''
            SELECT DISTINCT m2.name, ROUND(AVG(m.mark), 2) AS avg_mark
            FROM mark m
            LEFT JOIN subject s2 ON s2.id = m.subject_id
            LEFT JOIN mentor m2 ON m2.id = s2.mentor_id
            WHERE m2.id = %s
            GROUP BY m2.name;
            '''
    return get_data(request, (mentor_id,))
