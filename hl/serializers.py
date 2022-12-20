from django.db.models import fields
from rest_framework import serializers
from .models import HouseholdLedge

class HLSerializer(serializers.ModelSerializer):
    class Meta:
        model = HouseholdLedge
        fields = ('id', 'member_id', 'date', 'amount', 'memo')