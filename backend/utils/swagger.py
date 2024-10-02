from django.urls import path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from django.conf import settings

APP_PORT = settings.APP_PORT
# Swagger 配置
schema_view = get_schema_view(
    openapi.Info(
        title="范同学的个人博客接口文档",
        default_version='1.0.0',
        description="API文档",
        contact=openapi.Contact(email="2690931889@qq.com"),
        license=openapi.License(name="BSD License"),
        host="localhost:" + APP_PORT,
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('swagger.json', schema_view.without_ui(cache_timeout=0), name='schema-json'),  # JSON格式
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),  # Swagger UI
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),  # ReDoc UI
]

