from django.db import models

# Create your models here.

class Member(models.Model):
    id = models.BigAutoField(primary_key=True)
    email = models.CharField(unique=True, max_length=100)
    password = models.CharField(max_length=250)

    class Meta:
        managed = False
        db_table = 'member'