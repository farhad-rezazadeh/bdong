# Generated by Django 3.2.9 on 2021-11-11 15:48

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("groups", "0002_invite"),
    ]

    operations = [
        migrations.CreateModel(
            name="Expense",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("description", models.TextField()),
                ("created", models.DateTimeField(auto_now_add=True)),
                (
                    "total_cost",
                    models.DecimalField(
                        decimal_places=2,
                        default=0.0,
                        max_digits=12,
                        validators=[django.core.validators.MinValueValidator(0.0)],
                    ),
                ),
                (
                    "creator",
                    models.ForeignKey(
                        null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL
                    ),
                ),
                (
                    "group",
                    models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to="groups.group"),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Share",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                (
                    "share",
                    models.DecimalField(
                        decimal_places=2,
                        default=0.0,
                        max_digits=12,
                        validators=[django.core.validators.MinValueValidator(0.0)],
                    ),
                ),
                (
                    "paid",
                    models.DecimalField(
                        decimal_places=2,
                        default=0.0,
                        max_digits=12,
                        validators=[django.core.validators.MinValueValidator(0.0)],
                    ),
                ),
                ("expense", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to="expenses.expense")),
                ("user", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                "unique_together": {("user", "expense")},
            },
        ),
        migrations.AddField(
            model_name="expense",
            name="participants",
            field=models.ManyToManyField(
                related_name="participants",
                related_query_name="participants",
                through="expenses.Share",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]
