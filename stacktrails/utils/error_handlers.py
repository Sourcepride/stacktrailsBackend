from django.http import JsonResponse


def custom404(request, exception=None):
    return JsonResponse(
        {
            "status": "error",
            "status_code": 404,
            "message": "This Resource Was Not Found",
            "data": [],
        },
        status=404,
    )
