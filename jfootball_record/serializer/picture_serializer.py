from datetime import datetime

from rest_framework import serializers

from jfootball_record.model_definition.match_records_models import MatchRecords
from jfootball_record.model_definition.picture_models import Picture

class UploadedPictureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Picture
        fields = ['id','picture','record_id','uploaded_at']
        read_only_fields = ['record_id','uploaded_at']

    def get_record(self, obj,image=None):
        data=MatchRecords.objects.get(id=obj.record_id)
        return {
            "id": data.id,
            "title": data.title,
            "record": data.record,
            "home_team_id": data.home_team_id,
            "home_score": data.home_score,
            "away_team_id": data.away_team_id,
            "away_score": data.away_score,
            "round": data.round,
            "match_day": data.match_day,
            "image": image,
            "created_by_id": data.created_by_id,
        }

    def get_query_params(self):
        self.request = self.context.get('request')
        title=self.request.query_params.get('title')
        record=self.request.query_params.get('record')
        home_team_id=self.request.query_params.get('home_team_id')
        home_score=self.request.query_params.get('home_score')
        away_team_id=self.request.query_params.get('away_team_id')
        away_score=self.request.query_params.get('away_score')
        round=self.request.query_params.get('round')
        match_day=self.request.query_params.get('match_day')

        if type(title) is not str:
            raise serializers.ValidationError("title must be a string")   
        elif type(record) is not str:
            raise serializers.ValidationError("record must be a string")   
        elif type(int(home_score)) is not int:
            raise serializers.ValidationError("home_score must be an integer")   
        elif type(int(away_score)) is not int:
            raise serializers.ValidationError("away_score must be an integer")   
        elif type(int(round)) is not int:
            raise serializers.ValidationError("round must be an integer")   
        elif type(match_day) is not str:
            raise serializers.ValidationError("match_day must be a date")   
        elif len(title)>20:
            raise serializers.ValidationError("title must be less than 20 characters")
        elif len(record)>1000:
            raise serializers.ValidationError("record must be less than 1000 characters")
        elif len(home_score)>100 or len(away_score)>100:
            raise serializers.ValidationError("home_score and away_score must be less than 100 characters")
        elif len(home_team_id)>100 or len(away_team_id)>100:
            raise serializers.ValidationError("home_team_id and away_team_id must be less than 100 characters")
        
        return {
            "title": title,
            "record": record,
            "home_team_id": home_team_id,
            "home_score": home_score,
            "away_team_id": away_team_id,
            "away_score": away_score,
            "round": round,
            "match_day": datetime.strptime(match_day, '%Y-%m-%d'),
        }
        
        
    def create_record(self, user_id):
        data=self.get_query_params()
        record = MatchRecords.objects.create(
            title=data['title'],
            record=data['record'],
            home_team_id=data['home_team_id'],
            home_score=data['home_score'],
            away_team_id=data['away_team_id'],
            away_score=data['away_score'],
            round=data['round'],
            match_day=data['match_day'],
            created_by_id=user_id
        )
        try:
            record.save()
        except Exception as e:
            raise serializers.ValidationError("Failed to create record")
        return record

        

