
from django.urls import path
from jfootball_record.views.picture_views import PictureView
from jfootball_record.views.players_view import TeamPlayersView
from jfootball_record.views.user_views import UserView
from jfootball_record.views.league_views import LeagueRankingView
from jfootball_record.views.team_views import TeamDetailView, TeamListView
from jfootball_record.views.match_records_views import MatchRecordListView, MatchRecordsViewSet
from jfootball_record.views.comments_views import CommentsView
from jfootball_record.views.nice_views import NiceView
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
record_view =MatchRecordsViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'})
urlpatterns = [
    path('user', UserView.as_view()),
    path('records/<int:pk>/', record_view),
    path('comments/<int:record_id>', CommentsView.as_view()),
    path('picture/<int:record_id>', PictureView.as_view()),
    path('teams/<int:league_id>', TeamListView.as_view()),
    path('teams/detail/<int:team_id>', TeamDetailView.as_view()),
    path('league/ranking/<int:division_id>', LeagueRankingView.as_view()),
    path('palyers/detail/<int:team_id>/<int:player_id>', TeamPlayersView.as_view()),
    path('records/<int:record_id>/nice/',NiceView.as_view({"post": "create", "delete": "destroy","get": "list"})),
    path('records/list', MatchRecordListView.as_view())
]