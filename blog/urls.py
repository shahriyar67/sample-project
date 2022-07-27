from django.urls import path
from .views import ArticleList, ArticleDetail, AuthorList, CategoryList, SearchList

app_name = "blog"

urlpatterns = [
    path('', ArticleList.as_view(), name="list"),
    path('', ArticleList.as_view(), name="home"),
    path('category/<slug:slug>', CategoryList.as_view(), name="category"),
    path('category/<slug:slug>/page/<int:page>', CategoryList.as_view(), name="category"),
    path('search/', SearchList.as_view(), name="search"),
    path('search/page', SearchList.as_view(), name="search"),
    path('page/<int:page>', ArticleList.as_view(), name="home"),
    path('home/<slug:slug>', ArticleDetail.as_view(), name="detail"),
    path('author/<slug:username>', AuthorList.as_view(), name="author"),
    path('author/<slug:username>/page/<int:page>', AuthorList.as_view(), name="author")
]
