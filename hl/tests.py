from django.test import TestCase
from .serializers import HLSerializer
from .models import HouseholdLedge
from utils import encrytion
from datetime import datetime, timedelta

def day_ago_datetime(day):
    return datetime.now()-timedelta(days=day)

TEST_HL_DATA = {"member_id":1,"date":day_ago_datetime(-10),"amount":10000,"memo":"test"}
# Create your tests here.
class HLTest(TestCase):
    def test_no_sign_add(self):
        res = self.client.post("/hl/add/",TEST_HL_DATA)
        self.assertEqual(res.status_code, 401)
        
    def test_no_sign_edit(self):
        hl = HouseholdLedge.objects.create(member_id=1,date=datetime(2022,11,1),amount=10000,memo="test")
        res = self.client.post(f"/hl/edit/{hl.id}/",{"member_id":1,"date":datetime(2022,11,1),"amount":5000,"memo":"test"})
        # after_hl = HouseholdLedge.objects.get(pk=hl.id)
        # data = HLSerializer(after_hl)
        self.assertEqual(res.status_code, 401)
        # self.assertEqual(res.data["amount"], 5000)
        # self.assertEqual(res.data, data.data)
        
    def test_no_sign_detail(self):
        hl = HouseholdLedge.objects.create(member_id=1,date=datetime(2022,11,1),amount=10000,memo="test")
        data = HLSerializer(hl)
        res = self.client.get(f"/hl/detail/{hl.id}/")
        # self.assertEqual(data.data, res.data)
        self.assertEqual(res.status_code, 401)