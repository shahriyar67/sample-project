from django import template
from ..models import Category, Article
from django.template.loader import get_template
from datetime import datetime, timedelta
from django.db.models import Count, Q


register = template.Library()


@register.simple_tag
def tags():
    return Category.name


templateAdress = get_template("blog/partials/category_navbar.html")


@register.inclusion_tag(templateAdress)
def category_navbar():
    return {
        "category": Category.objects.filter(status=True)
    }


@register.inclusion_tag("registration/partials/link.html")
def link(request, link_name, content, classes):
    return {
        "request": request,
        "link_name": link_name,
        "link": "account:{}".format(link_name),
        "content": content,
        "classes": classes,
    }


# @register.inclusion_tag("blog/partials/popular_articles.html")
# def popular_articles():
#     last_month = datetime.today()-timedelta(days=30)
#     return {
#         "popular_articles": Article.objects.published().annotate(count=Count('hits', filter=Q(articlehits__created__gt=last_month))).order_by('-count', '-publish')[:5],
#         "title": "مقالات پر بازدید ماه"
#     }
    
    
# @register.inclusion_tag("blog/partials/hot_articles.html")
# def hot_articles():
#     last_month = datetime.today()-timedelta(days=30)
#     return {
#         "hot_articles": Article.objects.published().annotate(count=Count('comments', filter=Q(comments__posted__gt=last_month) and Q(comments__content_type_id=6))).order_by('-count', '-publish')[:5],
#         "title": "مقالات داغ ماه"
#     }