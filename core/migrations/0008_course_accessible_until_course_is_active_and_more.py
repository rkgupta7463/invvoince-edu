# Generated by Django 5.1.4 on 2025-01-09 11:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_course_owner'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='accessible_until',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='course',
            name='is_active',
            field=models.BooleanField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='course',
            name='course_duration',
            field=models.CharField(blank=True, choices=[('1_month', '1 Month'), ('2_months', '2 Months'), ('3_months', '3 Months'), ('6_months', '6 Months')], max_length=50, null=True),
        ),
    ]
