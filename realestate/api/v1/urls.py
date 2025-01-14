from django.urls import path, include
from rest_framework.routers import DefaultRouter
from api.v1.viewsets import SignupView, LoginView


urlpatterns = [
    path('property/', include('api.v1.property.urls')),
    path('signup/', SignupView.as_view(), name='signup'),
    path('login/', LoginView.as_view(), name='login'),
]
