from django.urls import path
from .views import ArticleList

app_name = "api"
urlpatterns = [
    path('list', ArticleList.as_view(), name="list")
]
