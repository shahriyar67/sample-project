from rest_framework.generics import ListCreateAPIView
from blog.models import Article
from .serializers import ArticleSerializer

# Create your views here.


class ArticleList(ListCreateAPIView):
    queryset= Article.objects.all().order_by("-published")
    serializer_class=ArticleSerializer