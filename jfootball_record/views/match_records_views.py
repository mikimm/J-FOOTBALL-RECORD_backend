from rest_framework import filters, viewsets,status
from rest_framework.response import Response
from jfootball_record.exception.exception_handler import hundle_exception
from jfootball_record.model_definition.match_records_models import MatchRecords
from jfootball_record.model_definition.nice_models import Nice
from jfootball_record.model_definition.teams_models import Teams
from jfootball_record.serializer.match_records_serializer import MatchRecordsSerializer
from rest_framework.pagination import PageNumberPagination
from django_filters import FilterSet,CharFilter
from django_filters.rest_framework import DjangoFilterBackend 

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
class MatchRecordsViewSet(viewsets.ModelViewSet):
    serializer_class = MatchRecordsSerializer
    queryset = MatchRecords.objects.all()
    #TODO:user_idの取得方法
    user_id=2
    #pagenation設定
    pagination_class = MyPagination
    #filtering設定
    filter_backends = [DjangoFilterBackend,filters.OrderingFilter]
    filterset_class = MatchRecordsFilter
    ordering_fields = ['id']
    #辞書更新プライベートメソッド
    def _update_dict(self,target:dict,add_data:dict):
        if not(type(target) is  dict and type(add_data) is dict):
            TypeError("target and add_data must be dict")
        target.update(add_data)
        
        
    def perform_create(self, serializer):
        serializer.save(created_by_id=self.user_id)

    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
        except Exception as e:
            return hundle_exception(e)
        created_by_id=instance.__getattribute__("created_by_id")
        if created_by_id==self.user_id:
            self.perform_destroy(instance)
        else:
            return Response("権限がありません",status=status.HTTP_403_FORBIDDEN)
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        
        try:
            instance = self.get_object()
        except Exception as e:
            return hundle_exception(e)
        created_by_id=instance.__getattribute__("created_by_id")
        
        if created_by_id==self.user_id:
            serializer = self.get_serializer(instance, data=request.data, partial=partial)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
        else:
            return Response("権限がありません",status=status.HTTP_403_FORBIDDEN)

        if getattr(instance, '_prefetched_objects_cache', None):
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)

    def list(self, request, *args, **kwargs):
        response=super().list(self,request, *args, **kwargs)
        results=response.data["results"]
        if len(results) == 0:
            return response
        all_teams_list=Teams.objects.all()
        for result in results:
            count=Nice.objects.filter(record_id=result["id"]).count()
            for team in all_teams_list:
                if not ("home_team_name" in result
                        and "away_team_name" in result
                        and "home_team_logo" in result
                        and "away_team_logo" in result):
                    result["nice_count"]=count
                    if result["home_team_id"] == team.id:
                        self._update_dict(result,{"home_team_name":team.team_name,"home_team_logo":team.team_logo})
                    elif result["away_team_id"] == team.id:
                        self._update_dict(result,{"away_team_name":team.team_name,"away_team_logo":team.team_logo})
                else:
                    break
        return response
