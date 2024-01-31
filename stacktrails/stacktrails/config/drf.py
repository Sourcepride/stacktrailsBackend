from datetime import timedelta

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework_simplejwt.authentication.JWTAuthentication"
    ],
    "DEFAULT_PAGINATION_CLASS": "utils.paginator.CustomPageNumberPagination",
    "PAGE_SIZE": 15,
    "DEFAULT_RENDERER_CLASSES": [
        "utils.renders.CustomRenderer",
        "rest_framework.renderers.BrowsableAPIRenderer",
    ],
}

# SIMPLEJWT
SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(hours=2),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=30),
    "ROTATE_REFRESH_TOKENS": True,
}
