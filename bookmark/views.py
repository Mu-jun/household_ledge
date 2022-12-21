from django.shortcuts import get_object_or_404
from rest_framework import status, serializers
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import BookmarkSerializer

from hl.models import HouseholdLedge
from .models import Bookmark

from utils import jwt_util
import jwt

# Create your views here.
@jwt_util.verify_access
def index(req):
    access_token = req.COOKIES["jwt"]
    # try:
    #     payload = jwt_util.verify(access_token)
    # except jwt.ExpiredSignatureError: #시간만료
    #     return redirect('refresh')
    # except jwt.InvalidTokenError: #유효하지 않은 토큰
    #     return Response(status=status.HTTP_401_UNAUTHORIZED)
    
    payload = jwt_util.verify(access_token)
    member_id = payload["id"]

    bookmark_list = Bookmark.objects.filter(member_id=member_id)
    data = BookmarkSerializer(bookmark_list)
    return Response(data.data)

@jwt_util.verify_access
def paste(req, id):
    access_token = req.COOKIES["jwt"]
    # try:
    #     payload = jwt_util.verify(access_token)
    # except jwt.ExpiredSignatureError: #시간만료
    #     return redirect('refresh')
    # except jwt.InvalidTokenError: #유효하지 않은 토큰
    #     return Response(status=status.HTTP_401_UNAUTHORIZED)
    
    payload = jwt_util.verify(access_token)
    member_id = payload["id"]
    
    bookmark = get_object_or_404(Bookmark, pk=id)
    data = BookmarkSerializer(bookmark)
    
    return Response(data.data)

@jwt_util.verify_access
def copy(req, id):
    access_token = req.COOKIES["jwt"]
    # try:
    #     payload = jwt_util.verify(access_token)
    # except jwt.ExpiredSignatureError: #시간만료
    #     return redirect('refresh')
    # except jwt.InvalidTokenError: #유효하지 않은 토큰
    #     return Response(status=status.HTTP_401_UNAUTHORIZED)
    
    payload = jwt_util.verify(access_token)
    member_id = payload["id"]
    
    #1
    hl = HouseholdLedge.objects.get(id=id)
    bookmark = Bookmark.objects.create({"member_id":member_id, "amount":hl.amout, "memo":hl.memo})
    data = BookmarkSerializer(bookmark)
    
    #2
    # req.data.member_id = member_id
    # data = BookmarkSerializer(data=req.data)
    return Response(data.data, status=201)

@jwt_util.verify_access
def delete(req, id):
    access_token = req.COOKIES["jwt"]
    # try:
    #     payload = jwt_util.verify(access_token)
    # except jwt.ExpiredSignatureError: #시간만료
    #     return redirect('refresh')
    # except jwt.InvalidTokenError: #유효하지 않은 토큰
    #     return Response(status=status.HTTP_401_UNAUTHORIZED)
    
    payload = jwt_util.verify(access_token)
    member_id = payload["id"]

    bookmark = get_object_or_404(Bookmark,pk=id)
    if bookmark.member_id == member_id:
        bookmark.delete()
        return Response()
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)