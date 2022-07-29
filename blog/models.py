from django.db import models
from django.utils import timezone
from account.models import User
# Create managers here.
class CategoryManager(models.Manager):
    def published(self):
        return self.filter(status=True)
    
class ArticleManager(models.Manager):
    def published(self):
        return self.filter(status=True)


# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=20, verbose_name="نام دسته بندی")
    parent = models.ForeignKey('self', null=True, blank=True, default=None,
                               on_delete=models.SET_NULL,
                               related_name='children', verbose_name='زیر دسته')
    position = models.IntegerField(verbose_name="پوزیشن")
    status = models.BooleanField(default=True, verbose_name="منتشر شود؟")
    slug = models.SlugField(max_length=100, unique=True,
                            verbose_name="اسلاگ دسته بندی")
    
    class Meta:
        ordering = ['parent__id', 'position']
        verbose_name = "دسته بندی"
        verbose_name_plural = "دسته بندی ها"

    def __str__(self):
        return self.name
    objects = CategoryManager()




class Article(models.Model):
    title=models.CharField(max_length=60)
    author=models.ForeignKey(User, on_delete=models.CASCADE, related_name='articles')
    description=models.TextField()
    thumbnail=models.ImageField(upload_to='images',null=True)
    created=models.DateTimeField(default=timezone.now)
    published=models.DateTimeField(auto_now_add=True)
    updated=models.DateTimeField(auto_now=True)
    status=models.BooleanField(default=False)
    slug=models.SlugField()
    Category = models.ManyToManyField(Category, related_name="articles")
    
    
    def __str__(self):
        return self.title
    
    objects = ArticleManager()