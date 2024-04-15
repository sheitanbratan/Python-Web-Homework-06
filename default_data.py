import random
from datetime import datetime, timedelta

from faker import Faker


subjects: dict[str, str] = {
    'Math': '', 'Literature': '',
    'English': '', 'Biology': '',
    'Physics': '', 'Chemistry': ''
}


groups: dict[str, list] = {
    'group_a': [],
    'group_b': [],
    'group_c': []
}


grades: dict[str, str] = {
    '1': '(Unsatisfactory)',
    '2': '(Bad)',
    '3': '(Satisfactory)',
    '4': '(Good)',
    '5': '(Excellent)'
}


grades_table = {}


Faker.seed(1)
fake: Faker = Faker('uk-UA')


def faker_func(quantity):
    """ fake data creating function """

    return [str(f'{fake.first_name()} {fake.last_name()}')
            for _ in range(quantity)]


def groups_filling(students) -> dict:
    """ separation students by their groups """

    for i, name in enumerate(students):
        if i % 3 == 0:
            groups['group_a'].append(name)
        elif i % 2 == 0:
            groups['group_b'].append(name)
        else:
            groups['group_c'].append(name)
    return groups


def subject_lecturers(lecturers) -> dict:
    """ separation lecturers by their subjects """

    for subject in subjects.keys():
        subjects[subject] = random.choice(lecturers)
    return subjects


students = faker_func(random.randint(35, 50))
lecturers = faker_func(5)


def grade_table_filling() -> dict:
    current_date = datetime.now()
    for st in students:
        grades_table[st] = {}
        for subject in subjects:
            grades_table[st][subject] = {
                'grades': [random.randint(1, 5) for _ in range(3)],
                'date': [(current_date - timedelta(days=random.randint(1, 365))).strftime('%Y-%m-%d') for _ in range(3)]
            }
    return grades_table

















