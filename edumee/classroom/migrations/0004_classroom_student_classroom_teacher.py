# Generated by Django 4.0.5 on 2022-07-06 20:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0005_rename_is_email_varified_user_is_email_verified'),
        ('classroom', '0003_remove_classroom_student_remove_classroom_teacher'),
    ]

    operations = [
        migrations.AddField(
            model_name='classroom',
            name='student',
            field=models.ManyToManyField(related_name='s_room', through='classroom.Membership', to='myapp.student'),
        ),
        migrations.AddField(
            model_name='classroom',
            name='teacher',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='room', to='myapp.teacher'),
        ),
    ]