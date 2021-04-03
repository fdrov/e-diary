#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import django
import time

import django.core.exceptions as exceptions

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project.settings")
django.setup()

import datacenter.models as models
import random



# schoolkid = models.Schoolkid.objects.get(full_name__contains='Фролов Иван Григорьевич')
# schoolkid_prime = models.Schoolkid.objects.get(full_name__contains='Савельев Епифан Валерьевич')
# print(schoolkid.year_of_study)
# print(schoolkid.group_letter)

commendation_examples = ['Молодец!', 'Отлично!', 'Хорошо!', 'Гораздо лучше, чем я ожидал!', 'Ты меня приятно удивил!', 'Великолепно!', 'Прекрасно!', 'Ты меня очень обрадовал!', 'Именно этого я давно ждал от тебя!', 'Сказано здорово - просто и ясно!', 'Ты, как всегда, точен!', 'Очень хороший ответ!', 'Талантливо!', 'Ты сегодня прыгнул выше головы!', 'Я поражен!', 'Уже существенно лучше!', 'Потрясающе!', 'Замечательно!', 'Прекрасное начало!', 'Так держать!', 'Ты на верном пути!', 'Здорово!', 'Это как раз то, что нужно!', 'Я тобой горжусь!', 'С каждым разом у тебя получается всё лучше!', 'Мы с тобой не зря поработали!', 'Я вижу, как ты стараешься!', 'Ты растешь над собой!', 'Ты многое сделал, я это вижу!', 'Теперь у тебя точно все получится!']

def get_schoolkid(first_last_name):
    try:
        schoolkid = models.Schoolkid.objects.get(full_name__contains=first_last_name)
        return schoolkid
    except (exceptions.MultipleObjectsReturned, exceptions.ObjectDoesNotExist) as err:
        print('Убедитесь, что правильно написали имя в формате «Фамилия Имя».', '\nОшибка:', err)


SCHOOLKID = get_schoolkid('Фролов Иван')


def fix_marks(schoolkid):
    for entry in models.Mark.objects.filter(schoolkid=schoolkid, points__in=[2,3]):
        entry.points = 5
        entry.save()


def remove_chastisements(schoolkid):
    models.Chastisement.objects.filter(schoolkid=schoolkid).delete()


def remove_commendations(schoolkid):
    models.Commendation.objects.filter(schoolkid=schoolkid).delete()

# remove_commendations(SCHOOLKID)


print('Похвалы Ваньке до:', [(commendation.text) for commendation in models.Commendation.objects.filter(schoolkid=SCHOOLKID)])


def create_commendation(schoolkid, lesson):
    last_lesson = models.Lesson.objects.filter(subject__title__contains=lesson,
                                               year_of_study=schoolkid.year_of_study,
                                               group_letter=schoolkid.group_letter).order_by('-date').first()
    is_commendation_exists = models.Commendation.objects.filter(created=last_lesson.date,
                                       schoolkid=SCHOOLKID,
                                       subject=last_lesson.subject,
                                       teacher=last_lesson.teacher).exists()
    if not is_commendation_exists:
        models.Commendation.objects.create(text=random.choice(commendation_examples),
                                           created=last_lesson.date,
                                           schoolkid=schoolkid,
                                           subject=last_lesson.subject,
                                           teacher=last_lesson.teacher)
    else:
        print(f'Похвала на урок {last_lesson.subject} от {last_lesson.date} уже существует.')
create_commendation(get_schoolkid('Фролов Иван'), 'Музыка')



# last_lesson = models.Lesson.objects.filter(subject__title__contains='Музыка',
#                                            year_of_study=SCHOOLKID.year_of_study,
#                                            group_letter=SCHOOLKID.group_letter).order_by('-date').first()
# print(models.Commendation.objects.filter(created=last_lesson.date,
#                                          schoolkid=SCHOOLKID,
#                                          subject=last_lesson.subject,
#                                          teacher=last_lesson.teacher).exists())
print('Похвалы Ваньке после:', [(commendation.text) for commendation in models.Commendation.objects.filter(schoolkid=SCHOOLKID)])

# models.Commendation.objects.create(text='Ты в ударе, Ванька',
#                                    created=lessons[0].date,
#                                    schoolkid=schoolkid,
#                                    subject=lessons[0].subject,
#                                    teacher=lessons[0].teacher)
