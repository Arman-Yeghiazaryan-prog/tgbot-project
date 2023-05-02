# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Armenian(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    word = models.TextField(db_column='Word')  # Field name made lowercase.
    translation = models.TextField(db_column='Translation')  # Field name made lowercase.
    source = models.TextField(db_column='Source')  # Field name made lowercase.

    class Meta:
        db_table = 'Armenian'


class English(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    word = models.TextField(db_column='Word')  # Field name made lowercase.
    translation = models.TextField(db_column='Translation')  # Field name made lowercase.
    source = models.TextField(db_column='Source')  # Field name made lowercase.

    class Meta:
        db_table = 'English'


class Users(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    userid = models.TextField(db_column='UserID', unique=True)  # Field name made lowercase.
    numtestsen = models.IntegerField(db_column='NumTestsEN', blank=True, null=True)  # Field name made lowercase.
    avgresen = models.FloatField(db_column='AvgResEN', blank=True, null=True)  # Field name made lowercase.
    numtestsam = models.IntegerField(db_column='NumTestsAM', blank=True, null=True)  # Field name made lowercase.
    avgresam = models.FloatField(db_column='AvgResAM', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        db_table = 'Users'
