# Generated by Django 4.1.5 on 2023-02-13 06:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0003_likepost_profile'),
    ]

    operations = [
        migrations.CreateModel(
            name='Follow',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_follow', models.CharField(max_length=100)),
                ('user_profile', models.CharField(max_length=100)),
            ],
        ),
    ]
