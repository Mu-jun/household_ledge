from django.http import QueryDict
from django.shortcuts import get_object_or_404, redirect
from rest_framework.response import Response
from rest_framework import status, serializers, parsers
from rest_framework.decorators import api_view, parser_classes
from .serializers import HLSerializer
from hl.models import HouseholdLedge
from utils import jwt_util, encrytion
from django.utils import timezone
import jwt, json

# Create your views here.
## 목차조회
@api_view(["GET"])
@jwt_util.verify_access
def index(req):
    access_token = req.COOKIES["jwt"]
    payload = jwt_util.verify(access_token)
    member_id = payload["id"]

    hl_list = HouseholdLedge.objects.filter(member_id=member_id)

    data = HLSerializer(hl_list)
    return Response(data.data)


## Household Ledge RUD
@api_view(["GET","PUT","DELETE"])
@jwt_util.verify_access
def household_ledge(req, id, **kwargs):
    if req.method == "GET":
        access_token = req.COOKIES["jwt"]
        payload = jwt_util.verify(access_token)
        member_id = payload["id"]

        hl = get_object_or_404(HouseholdLedge, id=id)
        if member_id == hl.member_id:
            data = HLSerializer(hl)
            return Response(data.data)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)

    if req.method == "PUT":
        access_token = req.COOKIES["jwt"]
        payload = jwt_util.verify(access_token)
        member_id = payload["id"]
        # print(req.body)
        # print(req.body.decode().replace("'",'"'))
        data = json.loads(req.body.decode().replace("'",'"'))
        # print(data)
        hl = get_object_or_404(HouseholdLedge, pk=id)
        if hl.member_id == member_id:
            updated_data = HLSerializer(hl, data=data)
            if updated_data.is_valid():
                updated_data.save()
                return Response(updated_data.data)
            else:
                print(updated_data.errors)
                return Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)

    if req.method == "DELETE":
        access_token = req.COOKIES["jwt"]
        payload = jwt_util.verify(access_token)
        member_id = payload["id"]

        hl = get_object_or_404(HouseholdLedge, pk=id)
        if hl.member_id == member_id:
            hl.delete()
            return Response(status=status.HTTP_202_ACCEPTED)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(["POST"])
@jwt_util.verify_access
def add(req):
    access_token = req.COOKIES["jwt"]
    payload = jwt_util.verify(access_token)
    member_id = payload["id"]

    data = QueryDict(f"member_id={member_id}", mutable=True)
    data.update(req.data)
    url_key = encrytion.make_hash_key(str(data))
    data.update({"url_key": url_key})
    data = HLSerializer(data=data)
    if data.is_valid():
        data.save()
        return Response(data.data, status=201)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
@jwt_util.verify_access
def edit(req, id):
    access_token = req.COOKIES["jwt"]
    payload = jwt_util.verify(access_token)
    member_id = payload["id"]

    hl = get_object_or_404(HouseholdLedge, pk=id)
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


@api_view(["GET"])
@jwt_util.verify_access
def delete(req, id):
    access_token = req.COOKIES["jwt"]
    payload = jwt_util.verify(access_token)
    member_id = payload["id"]

    hl = get_object_or_404(HouseholdLedge, pk=id)
    if hl.member_id == member_id:
        hl.delete()
        return Response(status=status.HTTP_202_ACCEPTED)
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)


## 공유하기
@api_view(["GET", "POST", "PUT"])
def share(req, url_key):
    if req.method == "GET":
        hl = get_object_or_404(HouseholdLedge, url_key=url_key)
        if (hl.url_key is not None) and (hl.url_key_expire_date < timezone.now()):
            return Response(status=status.HTTP_404_NOT_FOUND)

        date = HLSerializer(hl)
        return Response(date.data)

    if req.method == "POST" or req.method == "PUT":
        access_token = req.COOKIES["jwt"]
        try:
            payload = jwt_util.verify(access_token)
        except jwt.ExpiredSignatureError:  # 시간만료
            return redirect("refresh")
        except jwt.InvalidTokenError:  # 유효하지 않은 토큰
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        member_id = payload["id"]
        hl = get_object_or_404(HouseholdLedge, url_key=url_key)

        if hl.member_id == member_id:
            url_key_expire_date = req.POST["url_key_expire_date"]
            hl.url_key_expire_date = url_key_expire_date
            hl.save()
            return Response()
        else:
            return Response(status=status.HTTP_403_FORBIDDEN)
