from rest_framework import serializers

from django.db import models
from jfootball_record.model_definition.match_records_models import MatchRecords
from jfootball_record.serializer.teams_serializer import TeamsSerializer

# MatchRecords用シリアライザー
class MatchRecordsSerializer(serializers.ModelSerializer):
    home_team_id =serializers.IntegerField(min_value=1, max_value=60)
    away_team_id =serializers.IntegerField(min_value=1, max_value=60)
    created_by_id = serializers.IntegerField(read_only=True)
    class Meta:
        model=MatchRecords
        fields = ['id','title', 'record','home_team_id','home_score','away_team_id','away_score','round','match_day','created_by_id']
    def validate(self, data):
            """
            Check home_team and away_team.
            """
            if data['home_team_id'] == data['away_team_id']:
                raise serializers.ValidationError("away_team must be differnt from home_team")
            return data

class MatchRecordListSerializer(serializers.ModelSerializer):
    home_team = TeamsSerializer(read_only=True)
    away_team = TeamsSerializer(read_only=True)
    class Meta:
        model = MatchRecords
        fields = ['id', 'title', 'record', 'home_team', 'home_score', 'away_team', 'away_score', 'round', 'match_day', 'created_by_id']