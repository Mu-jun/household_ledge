# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Bookmark(models.Model):
    id = models.BigIntegerField(primary_key=True)
    member_id = models.BigIntegerField()
    amount = models.IntegerField()
    memo = models.CharField(max_length=1000)

    class Meta:
        managed = False
        db_table = 'bookmark'


class Householdledge(models.Model):
    id = models.BigIntegerField(primary_key=True)
    member_id = models.BigIntegerField()
    date = models.DateTimeField()
    amout = models.IntegerField()
    memo = models.CharField(max_length=1000)

    class Meta:
        managed = False
        db_table = 'householdledge'


class Member(models.Model):
    id = models.BigIntegerField(primary_key=True)
    email = models.CharField(max_length=100)
    password = models.CharField(max_length=250)

    class Meta:
        managed = False
        db_table = 'member'


class Shorturl(models.Model):
    short_url = models.CharField(primary_key=True, max_length=25)
    target_url = models.CharField(max_length=2100)
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'shorturl'