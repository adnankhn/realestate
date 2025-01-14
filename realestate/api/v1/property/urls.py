from django.urls import include, path
from api.v1.property.viewsets import PropertyViewSet, ShortlistView, UserPortfolioAPIView
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register("property-list", PropertyViewSet, basename="property-list"),

urlpatterns = [
    path("", include(router.urls)),
    path('shortlist',ShortlistView.as_view(), name="shortlist"),
    path('user-portfolio/', UserPortfolioAPIView.as_view(), name='user-portfolio'),


]
