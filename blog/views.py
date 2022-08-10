from django.shortcuts import get_object_or_404
from django.views.generic import ListView, DetailView
from .models import Article, Category
from account.models import User
from django.db.models import Q

# Create your views here.

class ArticleList(ListView):
     def get_queryset(self) :
         return Article.objects.filter(status=True).order_by("-published")
     paginate_by = 4


class ArticleDetail(DetailView):
    def get_object(self):
        slug = self.kwargs.get('slug')
        article = get_object_or_404(Article.objects.published(), slug=slug)
        # ip_address = self.request.user.ip_address
        # if ip_address not in article.hits.all():
        #     article.hits.add(ip_address)
        return article


class CategoryList(ListView):
    paginate_by = 5
    
    def get_queryset(self):
        slug = self.kwargs.get('slug')
        global category
        category = get_object_or_404(
            Category.objects.published(), slug=slug)
        return category.articles.published()
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = category
        return context


class SearchList(ListView):
    paginate_by = 5
    template_name = "blog/search.html"
    
    def get_queryset(self):
        search = self.request.GET.get('q')
        return Article.objects.filter(
            Q(description__icontains=search) | Q(title__icontains=search)
            )
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search'] = self.request.GET.get('q')
        return context


class AuthorList(ListView):
    paginate_by = 5
    template_name = 'blog/author_list.html'
    
    def get_queryset(self):
        global author
        username = self.kwargs.get('username')
        author = get_object_or_404(
            User, username=username)
        return author.articles.published()
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['author'] = author
        return context
    