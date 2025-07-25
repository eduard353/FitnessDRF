# Generated by Django 5.2.4 on 2025-07-16 10:21

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("trainers", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Schedule",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "day_of_week",
                    models.CharField(
                        choices=[
                            ("monday", "Понедельник"),
                            ("tuesday", "Вторник"),
                            ("wednesday", "Среда"),
                            ("thursday", "Четверг"),
                            ("friday", "Пятница"),
                            ("saturday", "Суббота"),
                            ("sunday", "Воскресенье"),
                        ],
                        help_text="День недели, в который проводится тренировка.",
                        max_length=10,
                        verbose_name="День недели",
                    ),
                ),
                (
                    "start_time",
                    models.TimeField(
                        help_text="Время начала тренировки (ЧЧ:ММ).",
                        verbose_name="Время начала",
                    ),
                ),
                (
                    "end_time",
                    models.TimeField(
                        help_text="Время окончания тренировки (ЧЧ:ММ).",
                        verbose_name="Время окончания",
                    ),
                ),
                (
                    "is_active",
                    models.BooleanField(
                        default=True,
                        help_text="Указывает, активно ли это расписание в данный момент.",
                        verbose_name="Активно",
                    ),
                ),
                (
                    "created_at",
                    models.DateTimeField(
                        auto_now_add=True, verbose_name="Дата создания расписания"
                    ),
                ),
                (
                    "updated_at",
                    models.DateTimeField(
                        auto_now=True,
                        verbose_name="Дата последнего обновления расписания",
                    ),
                ),
                (
                    "fitness_club",
                    models.ForeignKey(
                        help_text="Фитнес-клуб, в котором проходит тренировка.",
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="schedules",
                        to="trainers.fitnessclub",
                        verbose_name="Фитнес-клуб",
                    ),
                ),
                (
                    "trainer",
                    models.ForeignKey(
                        help_text="Тренер, для которого создано это расписание.",
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="schedules",
                        to="trainers.trainer",
                        verbose_name="Тренер",
                    ),
                ),
            ],
            options={
                "verbose_name": "Расписание",
                "verbose_name_plural": "Расписания",
                "ordering": ["day_of_week", "start_time"],
                "indexes": [
                    models.Index(
                        fields=["trainer", "day_of_week", "start_time"],
                        name="schedule_sc_trainer_153ca9_idx",
                    ),
                    models.Index(
                        fields=["fitness_club", "day_of_week"],
                        name="schedule_sc_fitness_a0bb43_idx",
                    ),
                ],
                "unique_together": {
                    ("trainer", "fitness_club", "day_of_week", "start_time", "end_time")
                },
            },
        ),
    ]
