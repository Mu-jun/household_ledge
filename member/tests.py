from django.test import TestCase
from .serializers import MemberSerializer
from .models import Member
from utils import encrytion
from datetime import datetime, timedelta

TEST_DATA1 = {"email":"dev@email.com", "password":"123"}
TEST_DATA2 = {"email":"dev@email.com", "password":"123123"}
TEST_DATA3 = {"email":"test@email.com", "password":"123123"}

# Create your tests here.
class MemberTest(TestCase):
    def test_sign_up(self):
        """
        가입 테스트
        """
        res = self.client.post("/member/signUp/",TEST_DATA1)
        self.assertEqual(res.status_code, 201)
        
        member = Member.objects.get(email=TEST_DATA1["email"])
        self.assertIsNotNone(member)


    def test_sign_up_conflict(self):
        """
        가입 시 동일 email 존재할 경우
        """
        res = self.client.post("/member/signUp/",TEST_DATA1)
        self.assertEqual(res.status_code, 201)
        
        res = self.client.post("/member/signUp/",TEST_DATA2)
        self.assertIsNotNone(res.status_code, 406)


    def test_sign_in(self):
        """
        로그인 성공 테스트
        """
        res = self.client.post("/member/signUp/",TEST_DATA1)
        res = self.client.post("/member/signIn/",TEST_DATA1)
        
        self.assertEqual(res.status_code, 202)

    def test_no_id_sign_in(self):
        """
        아이디가 존재하지 않을 경우
        """
        res = self.client.post("/member/signIn/",TEST_DATA1)
        
        self.assertEqual(res.status_code, 404)

    def test_wrong_password_sign_in(self):
        """
        비밀번호가 틀릴 경우
        """
        res = self.client.post("/member/signUp/",TEST_DATA1)
        res = self.client.post("/member/signIn/",TEST_DATA2)
        
        self.assertEqual(res.status_code, 400)


    def test_sign_out(self):
        """
        로그아웃 성공 테스트
        """
        res = self.client.post("/member/signUp/",TEST_DATA1)
        self.assertEqual(res.status_code, 201)
        
        res = self.client.post("/member/signIn/",TEST_DATA1)
        self.assertEqual(res.status_code, 202)
        
        res = self.client.get('/member/signOut')
        self.assertEqual(res.status_code, 200)


    def test_no_redirect_refresh(self):
        """
        리프레시 토큰 직접 접근 제한 테스트
        """
        res = self.client.post("/member/signUp/",TEST_DATA1)
        self.assertEqual(res.status_code, 201)
        
        res = self.client.post("/member/signIn/",TEST_DATA1)
        self.assertEqual(res.status_code, 202)
        
        res = self.client.get("/member/refresh/")
        self.assertEqual(res.status_code, 404)