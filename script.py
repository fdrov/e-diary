#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project.settings")
django.setup()

import django.core.exceptions as exceptions
import datacenter.models as models
import random

commendation_examples = ['Молодец!', 'Отлично!', 'Хорошо!', 'Гораздо лучше, чем я ожидал!', 'Ты меня приятно удивил!',
                         'Великолепно!', 'Прекрасно!', 'Ты меня очень обрадовал!', 'Именно этого я давно ждал от тебя!',
                         'Сказано здорово - просто и ясно!', 'Ты, как всегда, точен!', 'Очень хороший ответ!',
                         'Талантливо!', 'Ты сегодня прыгнул выше головы!', 'Я поражен!', 'Уже существенно лучше!',
                         'Потрясающе!', 'Замечательно!', 'Прекрасное начало!', 'Так держать!', 'Ты на верном пути!',
                         'Здорово!', 'Это как раз то, что нужно!', 'Я тобой горжусь!',
                         'С каждым разом у тебя получается всё лучше!', 'Мы с тобой не зря поработали!',
                         'Я вижу, как ты стараешься!', 'Ты растешь над собой!', 'Ты многое сделал, я это вижу!',
                         'Теперь у тебя точно все получится!']


def get_schoolkid(first_last_name):
    try:
        schoolkid = models.Schoolkid.objects.get(full_name__contains=first_last_name)
        return schoolkid
    except (exceptions.MultipleObjectsReturned, exceptions.ObjectDoesNotExist) as err:
        print('Убедитесь, что правильно написали имя в формате «Фамилия Имя».', '\nОшибка:', err)


def fix_marks(first_last_name):
    schoolkid = get_schoolkid(first_last_name)
    for entry in models.Mark.objects.filter(schoolkid=schoolkid, points__in=[2, 3]):
        entry.points = 5
        entry.save()


def remove_chastisements(first_last_name):
    schoolkid = get_schoolkid(first_last_name)
    models.Chastisement.objects.filter(schoolkid=schoolkid).delete()


def remove_commendations(first_last_name):
    schoolkid = get_schoolkid(first_last_name)
    models.Commendation.objects.filter(schoolkid=schoolkid).delete()


def create_commendation(first_last_name, lesson):
    schoolkid = get_schoolkid(first_last_name)
    last_lesson = models.Lesson.objects.filter(subject__title__contains=lesson,
                                               year_of_study=schoolkid.year_of_study,
                                               group_letter=schoolkid.group_letter).order_by('?').first()
    is_commendation_exists = models.Commendation.objects.filter(created=last_lesson.date,
                                                                schoolkid=schoolkid,
                                                                subject=last_lesson.subject,
                                                                teacher=last_lesson.teacher).exists()
    if not is_commendation_exists:
        models.Commendation.objects.create(text=random.choice(commendation_examples),
                                           created=last_lesson.date,
                                           schoolkid=schoolkid,
                                           subject=last_lesson.subject,
                                           teacher=last_lesson.teacher)
    else:
        print(f'Похвала на урок {last_lesson.subject} от {last_lesson.date} уже существует. Запусти функцию еще раз')
