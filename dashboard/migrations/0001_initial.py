# Generated by Django 3.1.6 on 2021-02-14 23:26

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Email',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.CharField(max_length=15)),
                ('subject', models.CharField(max_length=255)),
                ('body', models.TextField()),
                ('from_email', models.EmailField(max_length=254)),
                ('to_email', models.EmailField(max_length=254)),
            ],
        ),
    ]
