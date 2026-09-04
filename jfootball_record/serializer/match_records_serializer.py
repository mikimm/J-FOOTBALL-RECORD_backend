from rest_framework import serializers

from django.db import models
from jfootball_record.model_definition.match_records_models import MatchRecords
from jfootball_record.model_definition.nice_models import Nice
from jfootball_record.model_definition.teams_models import Teams
from jfootball_record.model_definition.users_models import Users
from jfootball_record.serializer.teams_serializer import TeamsSerializer
from django.contrib.auth import get_user_model
# MatchRecords用シリアライザー
class MatchRecordsSerializer(serializers.ModelSerializer):
    home_team_id =serializers.IntegerField(min_value=1, max_value=60)
    away_team_id =serializers.IntegerField(min_value=1, max_value=60)
    created_by_id = serializers.IntegerField(read_only=True)
    home_team= TeamsSerializer(read_only=True)
    away_team= TeamsSerializer(read_only=True)
    class Meta:
        model=MatchRecords
        fields = ['id','title', 'record','home_team_id','home_score','away_team_id','away_score','round','match_day','created_by_id','home_team','away_team']
    def validate(self, data):
            """
            Check home_team and away_team.
            """
            if data['home_team_id'] == data['away_team_id']:
                raise serializers.ValidationError("away_team must be differnt from home_team")
            return data
    def check_user(self,data,user_id):
            """
            Check Record and User
            """
            if user_id != data.created_by_id:
                raise serializers.ValidationError("not permissioned")
            return 

class MatchRecordListSerializer(serializers.ModelSerializer):
    home_team = TeamsSerializer(read_only=True)
    away_team = TeamsSerializer(read_only=True)
    user_name = serializers.SerializerMethodField()
    nice_count = serializers.SerializerMethodField()
    class Meta:
        model = MatchRecords
        fields = ['id', 'title', 'record', 'home_team', 'home_score', 'away_team', 'away_score', 'round', 'match_day', 'created_by_id','user_name','nice_count']
        

    def get_user_name(self, obj):
        user = Users.objects.get(id=obj.created_by_id)
        return user.username

    def get_nice_count(self, obj):
        nice_count = Nice.objects.filter(record_id=obj.id).count()
        return nice_count

