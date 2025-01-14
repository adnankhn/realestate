"""
URL configuration for realestate project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi


urlpatterns = [
    path("api/v1/", include("api.v1.urls")),
    path("admin/", admin.site.urls),
]

admin.site.site_header = "Real Estate Admin Portal"
admin.site.site_title = "Real Estate Admin"
admin.site.index_title = "Welcome to Real Estate Admin Portal"

# swagger
api_info = openapi.Info(
    title="Real Estate API",
    default_version="v1",
    description="API documentation for Real Estate",
)

schema_view = get_schema_view(
    api_info,
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns += [
    path("api-docs/", schema_view.with_ui("swagger", cache_timeout=0), name="api_docs")
]