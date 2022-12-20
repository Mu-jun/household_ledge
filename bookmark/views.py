from django.shortcuts import get_object_or_404
from rest_framework import status, serializers
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import BookmarkSerializer

from hl.models import HouseholdLedge
from .models import Bookmark

# Create your views here.
def index(req):
    member_id = 1

    bookmark_list = Bookmark.objects.filter(member_id=member_id)
    data = BookmarkSerializer(bookmark_list)
    return Response(data.data)

def paste(req, id):
    bookmark = get_object_or_404(Bookmark, pk=id)
    data = BookmarkSerializer(bookmark)
    
    return Response(data.data)

def add(req, id):
    member_id = 1
    
    req.data.member_id = member_id
    data = BookmarkSerializer(data=req.data)
    return Response(data.data, status=201)

def delete(req, id):
    member_id = 1

    bookmark = get_object_or_404(Bookmark,pk=id)
    if bookmark.member_id == member_id:
        bookmark.delete()
        return Response(status=status.HTTP_202_ACCEPTED)
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)