import os

from jfootball_record.serializer.match_records_serializer import MatchRecordsSerializer
from jfootball_record.serializer.picture_serializer import UploadedPictureSerializer
from rest_framework import generics
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.db import transaction


class CompletedRecordsView(generics.CreateAPIView):
    # authentication_classes = (SessionAuthentication,)
    # permission_classes = (IsAuthenticated, )
    def create(self,request, *args, **kwargs):
        record_serializer = MatchRecordsSerializer(data=request.data)
        picture_serializer = UploadedPictureSerializer(data=request.data)
        record_serializer.is_valid(raise_exception=True)
        user_id = self.request.user.id
        user_id = 1
        if not "picture" in request.data.keys() or not "caption" in request.data.keys():
            self.perform_create(record_serializer, picture_serializer, user_id,False)
        else:
            picture_serializer.is_valid(raise_exception=True)
            picture_serializer.check_file(request.FILES)
            self.perform_create(record_serializer, picture_serializer, user_id,True)
        headers = self.get_success_headers(record_serializer.data)
        return Response(record_serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, record_serializer, picture_serializer, user_id,picture_flag:bool):
        """対戦記録登録のみ"""
        if not picture_flag:
                record = record_serializer.save(
                    created_by_id=user_id
                )
        else:
            """画像登録と対戦記録登録"""
            with transaction.atomic():
                record = record_serializer.save(
                    created_by_id=user_id
                )
                picture_serializer.check_create(
                    data={"record_id":record.id,"user_id":user_id}
                )
                picture_serializer.save(
                    record=record
                )
