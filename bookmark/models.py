from django.db import models

# Create your models here.
class Bookmark(models.Model):
    id = models.BigAutoField(primary_key=True)
    member_id = models.BigIntegerField()
    amount = models.IntegerField()
    memo = models.CharField(max_length=1000)

    class Meta:
        managed = False
        db_table = 'bookmark'