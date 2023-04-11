from sqlalchemy import func, desc, select, and_

from database.models import Teacher, Student, Discipline, Grade, Group
from database.db import session


def select_one():
    """
    Знайти 5 студентів із найбільшим середнім балом з усіх предметів.
    SELECT s.fullname, ROUND(AVG(g.grade), 2) as avg_grade
    FROM grades g
    LEFT JOIN students s ON s.id = g.student_id
    GROUP BY s.id
    ORDER BY avg_grade DESC
    LIMIT 5;
    :return:
    """
    result = session.query(Student.fullname, func.round(func.avg(Grade.grade), 2).label('avg_grade'))\
             .select_from(Grade).join(Student).group_by(Student.id).order_by(desc('avg_grade')).limit(5).all()
    # order_by(Grade.grade.desc())
    return result


def select_two():
    """
    SELECT d.name, s.fullname, ROUND(AVG(g.grade), 2) as avg_grade
    FROM grades g
    LEFT JOIN students s ON s.id = g.student_id
    LEFT JOIN disciplines d ON d.id = g.discipline_id
    WHERE d.id = 5
    GROUP BY s.id
    ORDER BY avg_grade DESC
    LIMIT 1;
    :return:
    """
    result = session.query(
                        Discipline.name,
                        Student.fullname,
                        func.round(func.avg(Grade.grade), 2).label('avg_grade'))\
                    .select_from(Grade).join(Student).join(Discipline)\
                    .filter(Discipline.id == 5)\
                    .group_by(Student.id, Discipline.name).order_by(desc('avg_grade')).limit(1).first()
    return result


def select_3():
    """
    3 Знайти середній бал у групах з певного предмета.

        SELECT gr.name, d.name, ROUND(AVG(g.grade), 2) as avg_grade
        FROM grades g
        LEFT JOIN students s ON s.id = g.student_id
        LEFT JOIN disciplines d ON d.id = g.discipline_id
        LEFT JOIN [groups] gr ON gr.id = s.group_id
        WHERE d.id = 1
        GROUP BY gr.id
        ORDER BY avg_grade DESC;

    :return:
    """

    result = session.query(
                        Group.name,
                        Discipline.name,
                        func.round(func.avg(Grade.grade), 2).label('avg_grade'))\
                    .select_from(Grade).join(Discipline).join(Student).join(Group)\
                    .filter(Discipline.id == 2)\
                    .group_by(Group.id).order_by(desc('avg_grade')).all()
    return result

def select_4():
    """
    -- 4 Найти средний балл на потоке (по всей таблице оценок).

        SELECT ROUND(AVG(g.grade), 2) as avg_grade
        FROM grades g;

    :return:
    """

    result = session.query(func.round(func.avg(Grade.grade), 2).label('avg_grade'))\
                    .select_from(Grade).all()
    return result

def select_5():
    """
    -- 5 Найти какие курсы читает определенный преподаватель.

        SELECT d.name, t.fullname
        FROM disciplines d
        LEFT JOIN teachers t ON t.id = d.teacher_id
        WHERE t.id = 4
        GROUP BY d.id;

    :return:
    """

    result = session.query(Discipline.name, Teacher.fullname)\
                    .select_from(Discipline)\
                    .join(Teacher)\
                    .filter(Teacher.id == 3).order_by(Discipline.id).all()
    return result

def select_6():
    """
    -- 6 Найти список студентов в определенной группе.

        SELECT gr.name, s.fullname
        FROM [groups] gr
        LEFT JOIN students s ON s.group_id = gr.id
        WHERE gr.id = 2;

    :return:
    """

    result = session.query(Group.name, Student.fullname)\
                    .select_from(Group)\
                    .join(Student)\
                    .filter(Group.id == 2).all()
    return result

def select_7():
    """
    -- 7 Найти оценки студентов в отдельной группе по определенному предмету.

        SELECT gr.name, d.name, s.fullname, g.grade
        FROM grades g
        LEFT JOIN students s ON s.id = g.student_id
        LEFT JOIN disciplines d ON d.id = g.discipline_id
        LEFT JOIN [groups] gr ON gr.id = s.group_id
        WHERE d.id = 2 AND gr.id = 2;

    :return:
    """

    result = session.query(Group.name, Discipline.name, Student.fullname, Grade.grade)\
                    .select_from(Grade)\
                    .join(Student).join(Discipline).join(Group)\
                    .filter(and_(
                        Grade.discipline_id == 2, Student.group_id == 2)).all()
    return result

def select_8():
    """
    -- 8 Найти средний балл, который ставит определенный преподаватель по своим предметам.

        SELECT t.fullname, d.name, ROUND(AVG(g.grade), 2) as avg_grade
        FROM grades g
        LEFT JOIN disciplines d ON d.id = g.discipline_id
        LEFT JOIN teachers t ON t.id = d.teacher_id
        WHERE t.id = 4
        GROUP BY d.id;

    :return:
    """

    result = session.query(
                        Teacher.fullname,
                        Discipline.name,
                        func.round(func.avg(Grade.grade), 2).label('avg_grade'))\
                    .select_from(Grade).join(Discipline).join(Teacher)\
                    .filter(Teacher.id == 4)\
                    .group_by(Discipline.id).all()

    return result

def select_9():
    """
    -- 9 Найти список курсов, которые посещает определенный студент.

        SELECT s.fullname, d.name
        FROM disciplines d
        LEFT JOIN students s ON s.id = d.id
        WHERE s.id = 7
        ;

    :return:
    """

    result = session.query(Student.fullname, Discipline.name)\
                    .select_from(Grade)\
                    .join(Student).join(Discipline)\
                    .filter(Student.id == 22).all()
    return result


def select_10():
    """
    -- 10 Список курсов, которые определенному студенту читает определенный преподаватель.

        SELECT t.fullname, s.fullname, d.name
        FROM disciplines d
        LEFT JOIN students s ON s.id = d.id
        LEFT JOIN teachers t ON t.id = d.teacher_id
        WHERE s.id BETWEEN 2 AND 25

    :return:
    """

    result = session.query(Teacher.fullname, Student.fullname, Discipline.name)\
                    .select_from(Grade)\
                    .join(Discipline).join(Teacher).join(Student)\
                    .filter(and_(
                        Teacher.id == 3, Student.id == 2
                    )).all()
    return result


def select_11():
    """
    -- Средний балл, который определенный преподаватель ставит определенному студенту.



    :return:
    """

    result = session.query(
                        Teacher.id,
                        Student.fullname,
                        func.round(func.avg(Grade.grade), 2).label('avg_grade'))\
                        .select_from(Grade)\
                        .join(Student).join(Discipline).join(Teacher)\
                        .filter(and_(
                            Student.id == 3, Teacher.id == 3
                        )).all()

    # result = session.query(Student.id, Student.fullname, Grade.grade, Grade.date_of)\
    #                 .select_from(Grade)\
    #                 .join(Student)\
    #                 .filter(and_(
    #                     Grade.discipline_id == 3, Student.group_id == 3, Grade.date_of == subquery
    #                 ))\
    #                 .group_by(Student.id, Discipline.name).order_by(desc('avg_grade')).limit(1).first()
    return result


def select_12():
    """
    -- Оцінки студентів у певній групі з певного предмета на останньому занятті.
    select s.id, s.fullname, g.grade, g.date_of
    from grades g
    join students s on s.id = g.student_id
    where g.discipline_id = 3 and s.group_id = 3 and g.date_of = (
        select max(date_of)
        from grades g2
        join students s2 on s2.id = g2.student_id
        where g2.discipline_id = 3 and s2.group_id = 3
    );
    :return:
    """
    subquery = (select(func.max(Grade.date_of)).join(Student).filter(and_(
                    Grade.discipline_id == 3, Student.group_id == 3
                )).scalar_subquery())

    result = session.query(Student.id, Student.fullname, Grade.grade, Grade.date_of)\
                    .select_from(Grade)\
                    .join(Student)\
                    .filter(and_(
                        Grade.discipline_id == 3, Student.group_id == 3, Grade.date_of == subquery
                    )).all()
    return result


if __name__ == '__main__':
    # print(select_one())
    # print(select_two())
    # print(select_3()) # not worked
    # print(select_4())
    # print(select_5())
    # print(select_6())
    # print(select_7())
    # print(select_8()) # not worked
    # print(select_9())
    # print(select_10()) # working - а как такое может быть 0-0
    print(select_11()) # not worked
    # print(select_12())

