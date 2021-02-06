# Generated by Django 3.1.5 on 2021-02-05 03:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0003_auto_20210205_0256'),
    ]

    operations = [
        migrations.CreateModel(
            name='RequestToken',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.IntegerField()),
                ('code', models.CharField(default='8K0l1d6n7G3a3p7t7v8p4Y8z6B0v9S8Z8q0K0R6r2J9V8J4U5j2s9P4O4a9P', max_length=30, unique=True)),
            ],
        ),
        migrations.AlterField(
            model_name='authenticationrequest',
            name='code',
            field=models.CharField(default='3e3i6u5x5b1O1R1c6Q7Y4n6F4D2U1T3e8W8d6k3t9s3G1P8L8v5w1r6t9f1r', max_length=30, unique=True),
        ),
    ]
