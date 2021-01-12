from django.urls import path, include
from rest_framework.routers import DefaultRouter

from api.external_data import views

app_name = "external_data"

router = DefaultRouter()
router.register("denial", views.DenialViewSet, basename="denial")
router.register("denial-search", views.DenialSearchView, basename="denial_search")


urlpatterns = [
    path("", include(router.urls)),
]