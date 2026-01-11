from django.urls import path
from .views import home, rank_resumes

urlpatterns = [
    path("", home, name="home"),
    path("rank/", rank_resumes, name="rank"),
]