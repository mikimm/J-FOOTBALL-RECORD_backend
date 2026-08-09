from rest_framework import filters, generics, viewsets,status
from rest_framework.response import Response
from jfootball_record.exception.exception_handler import hundle_exception
from jfootball_record.model_definition.match_records_models import MatchRecords
from jfootball_record.model_definition.nice_models import Nice
from jfootball_record.model_definition.teams_models import Teams
from jfootball_record.serializer.match_records_serializer import MatchRecordListSerializer, MatchRecordsSerializer
from rest_framework.pagination import PageNumberPagination
from django_filters import FilterSet,CharFilter
from django_filters.rest_framework import DjangoFilterBackend
from jfootball_record.views.base_view_set import BaseViewSet 
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from distutils.util import strtobool
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
    
# Create your views here.
class MatchRecordsViewSet(BaseViewSet):
    authentication_classes = (SessionAuthentication,)
    permission_classes = (IsAuthenticated, )
    serializer_class = MatchRecordsSerializer
    queryset = MatchRecords.objects.all()
    
class MatchRecordListView(generics.ListAPIView):
    #pagenation設定
    pagination_class = MyPagination
    #filtering設定
    filter_backends = [DjangoFilterBackend,filters.OrderingFilter]
    filterset_class = MatchRecordsFilter
    authentication_classes = (SessionAuthentication,)
    permission_classes = (IsAuthenticated, )
    ordering_fields = ['id']
    serializer_class = MatchRecordListSerializer
    queryset = MatchRecords.objects.all().prefetch_related('home_team','away_team') 
    
    def get_queryset(self):
        if bool(strtobool(self.request.GET.get('mine'))):
            return MatchRecords.objects.filter(created_by=self.request.user.id).prefetch_related('home_team','away_team') 
        
 