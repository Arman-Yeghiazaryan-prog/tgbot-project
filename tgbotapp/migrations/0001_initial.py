# Generated by Django 4.2 on 2023-05-02 03:10

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Armenian',
            fields=[
                ('id', models.AutoField(db_column='ID', primary_key=True, serialize=False)),
                ('word', models.TextField(db_column='Word')),
                ('translation', models.TextField(db_column='Translation')),
                ('source', models.TextField(db_column='Source')),
            ],
            options={
                'db_table': 'Armenian',
            },
        ),
        migrations.CreateModel(
            name='English',
            fields=[
                ('id', models.AutoField(db_column='ID', primary_key=True, serialize=False)),
                ('word', models.TextField(db_column='Word')),
                ('translation', models.TextField(db_column='Translation')),
                ('source', models.TextField(db_column='Source')),
            ],
            options={
                'db_table': 'English',
            },
        ),
        migrations.CreateModel(
            name='Users',
            fields=[
                ('id', models.AutoField(db_column='ID', primary_key=True, serialize=False)),
                ('userid', models.TextField(db_column='UserID', unique=True)),
                ('numtestsen', models.IntegerField(blank=True, db_column='NumTestsEN', null=True)),
                ('avgresen', models.FloatField(blank=True, db_column='AvgResEN', null=True)),
                ('numtestsam', models.IntegerField(blank=True, db_column='NumTestsAM', null=True)),
                ('avgresam', models.FloatField(blank=True, db_column='AvgResAM', null=True)),
            ],
            options={
                'db_table': 'Users',
            },
        ),
    ]
