# Generated by Django 5.2.1 on 2025-05-11 17:18

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0005_poll_description_poll_title_alter_poll_department'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='vote',
            unique_together={('user', 'poll')},
        ),
    ]
