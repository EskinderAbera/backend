# Generated by Django 4.1.2 on 2022-10-15 11:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='sendermessage',
            name='isactive',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='sendermessage',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_message', to='core.sendermessage'),
        ),
    ]
