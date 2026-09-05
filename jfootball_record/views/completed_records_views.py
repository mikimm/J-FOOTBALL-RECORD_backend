import os

from jfootball_record.model_definition.match_records_models import MatchRecords
from jfootball_record.model_definition.picture_models import Picture
from jfootball_record.serializer.match_records_serializer import MatchRecordsSerializer
from jfootball_record.serializer.picture_serializer import UploadedPictureSerializer
from rest_framework import generics
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.db import transaction
from rest_framework import status, viewsets

class CompletedRecordsView(viewsets.ModelViewSet):
    # authentication_classes = (SessionAuthentication,)
    # permission_classes = (IsAuthenticated, )
    def create(self,request, *args, **kwargs):
        record_serializer = MatchRecordsSerializer(data=request.data)
        picture_serializer = UploadedPictureSerializer(data=request.data)
        record_serializer.is_valid(raise_exception=True)
        user_id = self.request.user.id
        user_id = 1
        if not "picture" in request.data.keys():
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

    def update(self, request, *args, **kwargs):
        record_serializer = MatchRecordsSerializer(data=request.data)
        picture_serializer = UploadedPictureSerializer(data=request.data)
        record_serializer.is_valid(raise_exception=True)
        self.request.user.id = 1
        #更新対象の記録instanceを取得
        record_instance = MatchRecords.objects.get(id=self.kwargs['record_id'])
        record_serializer.check_user(record_instance,self.request.user.id)
        #更新対象の画像instanceを取得
        picture_instance = None
        file_path = None
        if Picture.objects.filter(record_id=self.kwargs['record_id']).exists():
            picture_instance=Picture.objects.get(record_id=self.kwargs['record_id'])
            file_path=picture_instance.picture
        
        #pictureキーがなければ画像なしデータとして処理
        if not "picture" in request.data.keys():
            self.perform_update(record_serializer,picture_serializer,record_instance,picture_instance,file_path,False)
        else:
            picture_serializer.is_valid(raise_exception=True)
            picture_serializer.check_file(request.FILES)
            self.perform_update(record_serializer, picture_serializer,record_instance,picture_instance,file_path,True)
        headers = self.get_success_headers(record_serializer.data)
        return Response(record_serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    
    def perform_update(self, record_serializer, picture_serializer,record_instance,picture_instance,file_path,picture_flag:bool):
        """対戦記録登録のみ"""
        if not picture_flag:
                record_serializer.update(record_instance,record_serializer.validated_data)
                #既存画像をfilesystemから削除
                if self.request.data.get("picture_action")  == "delete":
                    if picture_instance is not None and file_path is not None:
                        Picture.objects.filter(record_id=self.kwargs['record_id']).delete()
                        picture_serializer.delete_filesystem(file_path)
        else:
            """画像登録と対戦記録更新"""
            with transaction.atomic():
                record_serializer.update(record_instance,record_serializer.validated_data)
                #既存画像があれば更新・なければ新規作成
                if picture_instance is not None:
                    picture_serializer.update(picture_instance,picture_serializer.validated_data)
                else:
                    picture_serializer.is_valid(raise_exception=True)
                    picture_serializer.check_file(self.request.FILES)
                    picture_serializer.save(record=record_instance)
                #新規画像をfilesystemに配置
                picture_serializer.set_filesystem(self.request.user.id)
                #既存画像をfilesystemから削除
                if file_path is not None:
                    picture_serializer.delete_filesystem(file_path)