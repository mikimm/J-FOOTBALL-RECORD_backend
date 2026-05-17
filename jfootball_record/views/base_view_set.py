from rest_framework import status, viewsets
from rest_framework.response import Response

from jfootball_record.exception.exception_handler import hundle_exception

class BaseViewSet(viewsets.ModelViewSet):
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