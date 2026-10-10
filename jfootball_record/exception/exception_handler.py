
from django.http import Http404, JsonResponse
from jfootball_record.exception.exceptions import ExternalAPIError, NotFoundError
from django.core.exceptions import ObjectDoesNotExist

def hundle_exception(exc:Exception) -> JsonResponse:

    if isinstance(exc, NotFoundError) or isinstance(exc, ObjectDoesNotExist) or isinstance(exc, Http404):
        return JsonResponse({"detail": str(exc)}, status=404)

    elif isinstance(exc, ExternalAPIError):
        return JsonResponse({"detail": str(exc)}, status=500)

    return JsonResponse({"detail": str(exc)}, status=500)