# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
from django.utils import timezone

class HouseholdLedge(models.Model):
    id = models.BigAutoField(primary_key=True)
    member_id = models.PositiveBigIntegerField()
    date = models.DateTimeField(default=timezone.now)
    amount = models.IntegerField()
    memo = models.CharField(max_length=1000)
    url_key = models.CharField(unique=True, max_length=25, blank=True, null=True)
    url_key_expire_date = models.DateTimeField(default=timezone.now)

    class Meta:
        managed = False
        db_table = 'householdledge'