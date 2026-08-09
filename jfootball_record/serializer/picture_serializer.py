from rest_framework import serializers

from jfootball_record.model_definition.match_records_models import MatchRecords
from jfootball_record.model_definition.picture_models import Picture

class UploadedPictureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Picture
        fields = ['id', 'caption', 'record_id','picture', 'uploaded_at']
        read_only_fields = ['record_id','uploaded_at']
    def check_create(self,data):
            """
            Check record_id and user_id.
            """
            record_id = data['record_id']
            user_id = data['user_id']
            if record_id is None:
                raise serializers.ValidationError("record_id is required")
            elif Picture.objects.filter(record_id=record_id).exists():
                raise serializers.ValidationError("picture already exists")
            elif not MatchRecords.objects.filter(id=record_id).exists():
                raise serializers.ValidationError("投稿がありません")
            elif MatchRecords.objects.get(id=record_id).created_by.id!=user_id:
                raise serializers.ValidationError("投稿権限がありません")
