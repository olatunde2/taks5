# videouploadapp/urls.py
from django.urls import path
from .views import upload_video

urlpatterns = [
    path('videos/', upload_video, name='videos'),
]
