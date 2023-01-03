from django.test import TestCase
from .serializers import HLSerializer
from .models import HouseholdLedge
from member.models import Member
from utils import encrytion, jwt_util
from datetime import datetime, timedelta
from django.utils import timezone

TEST_MEMBER_DATA = {"email": "dev@email.com", "password": "123"}


def day_ago_datetime(day):
    return timezone.now() - timedelta(days=day)


TEST_HL_DATA1 = {
    "member_id": 1,
    "date": day_ago_datetime(-10),
    "amount": 10000,
    "memo": "test",
}
TEST_HL_DATA2 = {"date": day_ago_datetime(-10), "amount": 10000, "memo": "test"}

# Create your tests here.
class HLTest(TestCase):
    def test_no_sign_add(self):
        """
        로그인 없이 가계부 쓰기 시도
        """
        res = self.client.post("/hl/add/", TEST_HL_DATA1)
        self.assertEqual(res.status_code, 401)

    def test_sign_in_add(self):
        """
        가입 >> 로그인 >> 가계부 쓰기
        """
        res = self.client.post("/member/signUp/", TEST_MEMBER_DATA)
        res = self.client.post("/member/signIn/", TEST_MEMBER_DATA)
        res = self.client.post("/hl/add/", TEST_HL_DATA2)

        self.assertEqual(res.data["amount"], TEST_HL_DATA2["amount"])
        self.assertEqual(res.data["memo"], TEST_HL_DATA2["memo"])
        self.assertEqual(res.status_code, 201)

    def test_no_sign_detail(self):
        """
        로그인 없이 가계부id로 가계부 상세보기 시도
        """
        member = Member.objects.create(
            email=TEST_MEMBER_DATA["email"], password=TEST_MEMBER_DATA["password"]
        )
        hl = HouseholdLedge.objects.create(
            member_id=member.id,
            date=TEST_HL_DATA2["date"],
            amount=TEST_HL_DATA2["amount"],
            memo=TEST_HL_DATA2["memo"],
        )
        res = self.client.get(f"/hl/{hl.id}/")
        # self.assertEqual(hl, res.data)
        self.assertEqual(res.status_code, 401)

    def test_sign_in_detail(self):
        """
        로그인 >> 가계부id로 가계부 상세보기
        """
        hashed_pw = encrytion.make_hashed_pw(TEST_MEMBER_DATA["password"])
        member = Member.objects.create(
            email=TEST_MEMBER_DATA["email"], password=hashed_pw
        )
        hl = HouseholdLedge.objects.create(
            member_id=member.id,
            date=TEST_HL_DATA2["date"],
            amount=TEST_HL_DATA2["amount"],
            memo=TEST_HL_DATA2["memo"],
        )

        res = self.client.post("/member/signIn/", TEST_MEMBER_DATA)

        res = self.client.get(f"/hl/{hl.id}/")
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.data["memo"], hl.memo)

    def test_no_sign_edit(self):
        """
        로그인 없이 가계부 수정 시도
        """
        hl = HouseholdLedge.objects.create(
            member_id=1, date=TEST_HL_DATA2["date"], amount=10000, memo="test"
        )
        res = self.client.post(
            f"/hl/edit/{hl.id}/",
            {
                "member_id": 1,
                "date": TEST_HL_DATA2["date"],
                "amount": 5000,
                "memo": "test",
            },
        )
        self.assertEqual(res.status_code, 401)

    def test_sign_in_edit1(self):
        """
        로그인 >> 가계부 쓰기 >> 가계부 수정 1
        """
        hashed_pw = encrytion.make_hashed_pw(TEST_MEMBER_DATA["password"])
        member = Member.objects.create(
            email=TEST_MEMBER_DATA["email"], password=hashed_pw
        )
        hl = HouseholdLedge.objects.create(
            member_id=member.id,
            date=TEST_HL_DATA2["date"],
            amount=TEST_HL_DATA2["amount"],
            memo=TEST_HL_DATA2["memo"],
        )

        res = self.client.post("/member/signIn/", TEST_MEMBER_DATA)
        self.assertEqual(res.status_code, 202)

        res = self.client.post(
            f"/hl/edit/{hl.id}/",
            {"member_id": member.id, "date": hl.date, "amount": 5000, "memo": hl.memo},
        )
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.data["amount"], 5000)

    def test_sign_in_edit2(self):
        """
        로그인 >> 가계부 쓰기 >> 가계부 수정 2
        """
        hashed_pw = encrytion.make_hashed_pw(TEST_MEMBER_DATA["password"])
        member = Member.objects.create(
            email=TEST_MEMBER_DATA["email"], password=hashed_pw
        )

        res = self.client.post("/member/signIn/", TEST_MEMBER_DATA)
        self.assertEqual(res.status_code, 202)
        res = self.client.post("/hl/add/", TEST_HL_DATA2)
        self.assertEqual(res.status_code, 201)
        self.assertEqual(res.data["amount"], TEST_HL_DATA2["amount"])

        hl = res.data

        res = self.client.put(
            f"/hl/{hl['id']}/",
            {
                "member_id": member.id,
                "date": hl["date"],
                "amount": 5000,
                "memo": hl["memo"],
            },
        )
        self.assertEqual(res.status_code, 200)
        # print(res.data)
        self.assertEqual(res.data["amount"], 5000)

    def test_shared(self):
        """
        공유활성화 >> 비로그인 접속
        """
        hashed_pw = encrytion.make_hashed_pw(TEST_MEMBER_DATA["password"])
        member = Member.objects.create(
            email=TEST_MEMBER_DATA["email"], password=hashed_pw
        )

        res = self.client.post("/member/signIn/", TEST_MEMBER_DATA)
        self.assertEqual(res.status_code, 202)

        res = self.client.post("/hl/add/", TEST_HL_DATA2)
        self.assertEqual(res.status_code, 201)
        self.assertEqual(res.data["amount"], TEST_HL_DATA2["amount"])

        hl = res.data

        hl.update(
            {"url_key_expire_date": (timezone.now() + timedelta(days=10)).isoformat()}
        )
        res = self.client.put(f"/hl/{hl['id']}/", hl)
        # print(res)
        updated_data = res.data
        # print(updated_data)

        res = self.client.get("/member/signOut/", TEST_MEMBER_DATA)

        res = self.client.get(f"/hl/{hl['url_key']}")
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.data["memo"], updated_data["memo"])
