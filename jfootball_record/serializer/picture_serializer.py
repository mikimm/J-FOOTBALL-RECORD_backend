from rest_framework import serializers

from jfootball_record.model_definition.match_records_models import MatchRecords
from jfootball_record.model_definition.picture_models import Picture

class UploadedPictureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Picture
        fields = ['id', 'caption', 'record','picture', 'uploaded_at']
        read_only_fields = ['record','uploaded_at']
    def check_create(self, data):
            """
            Check record exist
            """
            if Picture.objects.filter(record_id=data['record_id']).exists():
                raise serializers.ValidationError("picture already exists")
            if MatchRecords.objects.get(id=data['record_id']).created_by.id!=data['user_id']:
                raise serializers.ValidationError("投稿権限がありません")
