from django.test import TestCase
from .serializers import HLSerializer
from .models import HouseholdLedge

from datetime import datetime

# Create your tests here.
class HLTest(TestCase):
    def test_add(self):
        res = self.client.post("/hl/add/",{"member_id":1,"date":datetime(2022,11,1),"amount":10000,"memo":"test"})
        self.assertEqual(res.status_code, 201)
        
    def test_edit(self):
        hl = HouseholdLedge.objects.create(member_id=1,date=datetime(2022,11,1),amount=10000,memo="test")
        res = self.client.post(f"/hl/edit/{hl.id}/",{"member_id":1,"date":datetime(2022,11,1),"amount":5000,"memo":"test"})
        after_hl = HouseholdLedge.objects.get(pk=hl.id)
        data = HLSerializer(after_hl)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.data["amount"], 5000)
        self.assertEqual(res.data, data.data)
        
    def test_detail(self):
        hl = HouseholdLedge.objects.create(member_id=1,date=datetime(2022,11,1),amount=10000,memo="test")
        data = HLSerializer(hl)
        res = self.client.get(f"/hl/{hl.id}/")
        self.assertEqual(data.data, res.data)
        self.assertEqual(res.status_code, 200)