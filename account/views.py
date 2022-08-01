from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import (
    ListView,
    CreateView,
    UpdateView,
    DeleteView
)
from blog.models import Article
from django.urls import reverse_lazy
from .mixins import (
    FieldMixins,
    FormValidMixin,
    AuthorAccessMixin,
    AuthorsAccessMixin,
    SuperUserAccessMixin
)
from django.shortcuts import get_object_or_404
from .models import User
from .forms import ProfileForm
from django.contrib.auth.views import LoginView


from django.http import HttpResponse
from .forms import SignUpForm
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_active_token
from django.core.mail import EmailMessage
# Create your views here.

class ArticleList(LoginRequiredMixin, AuthorsAccessMixin, ListView):
    template_name = "registration/home.html"
    
    def get_queryset(self):
        if self.request.user.is_superuser:
            return Article.objects.all()
        else:
            return Article.objects.filter(author=self.request.user)


class ArticleCreate(LoginRequiredMixin, AuthorsAccessMixin, FormValidMixin, FieldMixins, CreateView):
    model = Article
    template_name = 'registration/Article_create_update.html'
    success_url = reverse_lazy('account:home')

class ArticleUpdate(AuthorAccessMixin, AuthorsAccessMixin, FormValidMixin, FieldMixins, UpdateView):
    model = Article
    template_name = 'registration/Article_create_update.html'
    

class ArticleDelete(SuperUserAccessMixin, DeleteView):
    model = Article
    success_url = reverse_lazy('account:home')
    template_name = 'registration/article_delete.html'


class ArticlePreview(AuthorsAccessMixin, DeleteView):
    def get_object(self) :
        pk = self.kwargs.get('pk')
        return get_object_or_404 (Article,pk=pk)
    template_name = 'registration/article_confirm_delete.html'


class Profile(LoginRequiredMixin, UpdateView):
    model = User
    template_name = 'registration/profile.html'
    success_url = reverse_lazy('account:profile')
    form_class = ProfileForm
    def get_object(self):
        return User.objects.get(pk=self.request.user.pk)
    
    def get_form_kwargs(self):
        kwargs = super(Profile, self).get_form_kwargs()
        kwargs.update({
            'user': self.request.user
        })
        return kwargs


class Login(LoginView):
    def get_success_url(self):
        user = self.request.user
        if user.is_superuser or user.is_author:
            return reverse_lazy("account:home")
        else :
            return reverse_lazy("account:profile")


class Register(CreateView):
    form_class = SignUpForm
    template_name = "registration/register.html"
    

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_active = False
        user.save()
        current_site = get_current_site(self.request)
        mail_subject = 'اکانت خود را فعال کنید...'
        message = render_to_string('registration/activate_account.html', {
            'user': user,
            'domain': current_site.domain,
            'uid':urlsafe_base64_encode(force_bytes(user.pk)),
            'token':account_active_token.make_token(user),
        })
        to_email = form.cleaned_data.get('email')
        email = EmailMessage(
                    mail_subject, message, to=[to_email]
        )
        email.send()
        return HttpResponse('لطفا آدرس ایمیل خود را تایید کنید تا ثبت نامک شما کامل شود')
        
def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_active_token.check_token(user, token):
        user.is_active = True
        user.save()
        
        return HttpResponse('به خواطر تایید ایمیلتان متشکریم. شما <a href="/login">الان میتوانید وارد اکانت خود شوید</a>')
    else:
        return HttpResponse('لینک فعال سازی معتبر نمی باشد.<a href="/login">لطفا دوباره تلاش کنید</a>')