from django.shortcuts import get_object_or_404, redirect
from rest_framework import status, serializers
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import MemberSerializer
from .models import Member
import jwt
from utils import encrytion, jwt_util
from datetime import datetime
from env import config

# Create your views here.
@api_view(["POST"])
def sign_up(req):
    email = req.POST["email"]
    password = req.POST["password"]
    
    member = get_object_or_404(Member, email=email)
    if(member):
        return Response(status=status.HTTP_406_NOT_ACCEPTABLE)
    
    hashed_pw = encrytion.make_hashed_pw(password)
    Member.objects.create({"email":email, "password":hashed_pw})
    
    return Response(status=status.HTTP_201_CREATED)

@api_view(["POST"])
def sign_in(req):
    email = req.POST["email"]
    password = req.POST["password"]
    
    member = Member.objects.get(email=email)
    if member is None:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    hashed_pw = encrytion.make_hashed_pw(password)
    if member.password == hashed_pw:
        payload = {"id":member.id, "email":email}
        access_token = jwt_util.create_access_token(payload)
        refresh_token = jwt_util.create_refresh_token(payload)
        
        req.session["jwt"] = refresh_token
        res = Response(status=status.HTTP_202_ACCEPTED)
        res.set_cookie("jwt", access_token, expires=datetime.utcnow()+config.TOKEN_MAXAGE, httponly=True, samesite="Lax")
        return res
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)

def sign_out(req):
    res = Response()
    res.delete_cookie("jwt")
    del req.session["jwt"]
    return res

def refresh(req):
    refresh_token = req.session["jwt"]
    try:
        payload = jwt_util.verify(refresh_token)
    except jwt.ExpiredSignatureError: #시간만료
        return Response(status=status.HTTP_401_UNAUTHORIZED)
    except jwt.InvalidTokenError: #유효하지 않은 토큰
        return Response(status=status.HTTP_401_UNAUTHORIZED)

    del payload["exp"]
    access_token = jwt_util.create_access_token(payload)

    res = redirect(req.META.get('HTTP_REFERER'))
    res.set_cookie("jwt", access_token, expires=datetime.utcnow()+config.TOKEN_MAXAGE, httponly=True, samesite="Lax")
    return res

