
from django.urls import path
from jfootball_record.views.completed_records_views import CompletedRecordsView
from jfootball_record.views.picture_views import PictureView
from jfootball_record.views.players_view import TeamPlayersView
from jfootball_record.views.league_views import LeagueRankingView
from jfootball_record.views.team_views import TeamDetailView, TeamListView
from jfootball_record.views.match_records_views import MatchRecordListView, MatchRecordsViewSet, MatchResultListView
from jfootball_record.views.comments_views import CommentsView
from jfootball_record.views.nice_views import NiceView
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
record_view_register =CompletedRecordsView.as_view({'post': 'create'})
record_view_revise =CompletedRecordsView.as_view({'put': 'update'})
record_view_operator =MatchRecordsViewSet.as_view({'get': 'retrieve',  'delete': 'destroy'})
urlpatterns = [
    #投稿機能
    path('completed_records/', record_view_register),
    path('completed_records/<int:record_id>/', record_view_revise),
    path('records/<int:pk>/', record_view_operator),
    path('picture/<int:record_id>', PictureView.as_view()),
    #コメント機能
    path('comments/<int:record_id>', CommentsView.as_view()),
    #リーグ別チーム一覧
    path('teams/<int:league_id>', TeamListView.as_view()),
    #チーム詳細
    path('teams/detail/<int:team_id>', TeamDetailView.as_view()),
    #リーグ順位
    path('league/ranking/<int:division_id>', LeagueRankingView.as_view()),
    #選手詳細情報
    path('palyers/detail/<int:team_id>/<int:player_id>', TeamPlayersView.as_view()),
    #いいね機能
    path('records/<int:record_id>/nice/',NiceView.as_view({"post": "create", "delete": "destroy","get": "list"})),
    #投稿一覧
    path('records/list', MatchRecordListView.as_view()),
    #試合結果一覧
    path('match/result/<int:team_id>',MatchResultListView.as_view())
]