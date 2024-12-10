from typing import Any
from . import models
from account.models import User
from django.shortcuts import get_object_or_404
from account.mixins import AuthorAccessMixin
from django.views.generic import ListView, DetailView, TemplateView
from desine.models import Image
# Create your views here.

class ArticleList(ListView):
    queryset = models.Article.objects.published().order_by("-created", "-updated")
    paginate_by = 2
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['img'] = Image.objects.get(id=1).img.url
        return context

class ArticleDetail(DetailView):
    def get_object(self):
        slug = self.kwargs.get('slug')
        article = get_object_or_404(models.Article.objects.published(), slug=slug)

        ip_address = self.request.user.ip_address
        if ip_address not in article.hits.all():
            article.hits.add(ip_address);

        return article

class ArticlePreview(AuthorAccessMixin, DetailView):
    model = models.Article
    
    def get_obj(self):
        pk = self.kwargs['pk']
        return get_object_or_404(models.Article, pk=pk, status="d"),

class CategoryList(ListView):
    template_name = 'blog/category_list.html'
    paginate_by = 2
    
    def get_queryset(self):
        global category
        slug = self.kwargs['slug']
        category = get_object_or_404(models.Category.objects.active(), slug=slug)
        return category.articles.published()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = category
        context['img'] = Image.objects.get(id=1).img.url
        return context

class AuthorList(ListView):
    template_name = 'blog/author_list.html'
    paginate_by = 2
    
    def get_queryset(self):
        global author
        username = self.kwargs['username']
        author = get_object_or_404(User, username=username)
        return author.articles.published()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['author'] = author
        context['img'] = Image.objects.get(id=1).img.url
        return context

class ProfileIconTemplate(TemplateView):
    template_name = 'blog/partials/profile_icon.html'
