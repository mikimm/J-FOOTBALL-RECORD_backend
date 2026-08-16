from django.db import models

from jfootball_record.model_definition.match_records_models import MatchRecords

class Picture(models.Model):
    caption = models.CharField(max_length=255)
    record = models.OneToOneField(MatchRecords,on_delete=models.CASCADE)
    picture = models.FileField(upload_to='uploads/') # 保存先を指定
    uploaded_at = models.DateTimeField(auto_now_add=True) #インスタンスを生成する際に更新される