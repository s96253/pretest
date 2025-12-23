from functools import wraps
from django.http import JsonResponse

ACCEPTED_TOKEN = "omni_pretest_token"


def require_valid_token(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        data = getattr(request, "data", {})
        token = data.get("token")

        if token != ACCEPTED_TOKEN:
            return JsonResponse({"detail": "Invalid token"}, status=403)

        return view_func(request, *args, **kwargs)

    return _wrapped_view
