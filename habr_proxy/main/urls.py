from django.urls import re_path
from .views import SiteProxyView


urlpatterns = [
    re_path('', SiteProxyView.as_view()),
]