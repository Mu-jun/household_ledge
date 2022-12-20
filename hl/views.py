from django.shortcuts import get_object_or_404
from rest_framework import status, serializers
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import HLSerializer
from hl.models import HouseholdLedge

# Create your views here.
@api_view(['GET'])
def index(req):
    member_id = 1
    
    hl_list = HouseholdLedge.objects.filter(member_id=member_id)
    
    data = HLSerializer(hl_list)
    return Response(data.data)

@api_view(['GET'])
def detail(req, id):
    hl = get_object_or_404(HouseholdLedge, pk=id)
    
    data = HLSerializer(hl)
    return Response(data.data)

@api_view(['POST'])
def add(req):
    member_id = 1
    
    req.data.member_id = member_id
    data = HLSerializer(data=req.data)
    if data.is_valid():
        data.save()
        return Response(data.data, status=201)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def edit(req, id):
    member_id = 1

    hl = get_object_or_404(HouseholdLedge,pk=id)
    if hl.member_id == member_id:
        data = HLSerializer(hl, data=req.data)
        if data.is_valid():
            data.save()
            return Response(data.data)
        else:
            print(data.errors)
            return Response(status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
def delete(req, id):
    member_id = 1

    hl = get_object_or_404(HouseholdLedge,pk=id)
    if hl.member_id == member_id:
        hl.delete()
        return Response(status=status.HTTP_202_ACCEPTED)
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)