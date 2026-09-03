from jfootball_record.exception.exception_handler import hundle_exception
from jfootball_record.usecase.match_usecase import match_usecase_handle
from rest_framework import filters, generics
from rest_framework.response import Response
from jfootball_record.model_definition.match_records_models import MatchRecords
from jfootball_record.serializer.match_records_serializer import MatchRecordListSerializer, MatchRecordsSerializer
from rest_framework.pagination import PageNumberPagination
from django_filters import FilterSet,CharFilter
from django_filters.rest_framework import DjangoFilterBackend
from jfootball_record.views.base_view_set import BaseViewSet 
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from jfootball_record.model_definition.picture_models import Picture
from distutils.util import strtobool
from rest_framework.views import APIView
from django.http import JsonResponse
from rest_framework import status
class MyPagination(PageNumberPagination):
    REST_FRAMEWORK = {
        'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
        'PAGE_SIZE': 100
    }
    page_size = 5
    def get_paginated_response(self, data):
        return Response({
            'current' :self.page.number,              # 現在のページ
            'count': self.page.paginator.count,       # 項目数の合計
            'final': self. page.paginator.num_pages,  # 全体のページ数
            'next': self.get_next_link(),             # 次のページネーションへのリンク
            'previous': self.get_previous_link(),  # 前のページネーションへのリンク
            'results': data,                       # 結果データ（page_size個のデータ）
        })

class MatchRecordsFilter(FilterSet):
    title = CharFilter(lookup_expr="icontains")

    class Meta:
        model = MatchRecords
        fields = ["title"]
    

class MatchRecordsViewSet(BaseViewSet):
    # authentication_classes = (SessionAuthentication,)
    # permission_classes = (IsAuthenticated, )
    serializer_class = MatchRecordsSerializer
    queryset = MatchRecords.objects.all()
    
    def get_picture(self, record_id,return_data,image_flag):
        if not image_flag:
            return_data.update({"file":{"image":"/media/uploads/NO_IMAGE.jpg"}})
            return Response(return_data)
        else: 
            picture=Picture.objects.get(record_id=record_id)
            return_data.update({"file":{"image":picture.picture.url}})
            return Response(return_data)
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return_data=serializer.data
        if Picture.objects.filter(record_id=return_data["id"]).exists():
            return self.get_picture(return_data["id"],return_data,True)
        else:
            return self.get_picture(return_data["id"],return_data,False)
    
class MatchRecordListView(generics.ListAPIView):
    #pagenation設定
    pagination_class = MyPagination
    #filtering設定
    filter_backends = [DjangoFilterBackend,filters.OrderingFilter]
    filterset_class = MatchRecordsFilter
    # authentication_classes = (SessionAuthentication,)
    # permission_classes = (IsAuthenticated, )
    ordering_fields = ['id']
    serializer_class = MatchRecordListSerializer
    queryset = MatchRecords.objects.all().prefetch_related('home_team','away_team') 
    
    def get_queryset(self):
        if self.request.GET.get('mine') and bool(strtobool(self.request.GET.get('mine'))):
            return MatchRecords.objects.filter(created_by=self.request.user.id).prefetch_related('home_team','away_team') 
        else:
            return MatchRecords.objects.all().prefetch_related('home_team','away_team')
        
class MatchResultListView(APIView):
    # authentication_classes = (SessionAuthentication,)
    # permission_classes = (IsAuthenticated, )
    def get(self, request, *args, **kwargs):
        try:
            output=match_usecase_handle(team_id=self.kwargs['team_id'])
        except Exception as e:
            return hundle_exception(e)
        return JsonResponse(output,safe=False)
        
 