from django.urls import path
from . import views

app_name = 'blog'
urlpatterns = [
    path('', views.ArticleList.as_view(), name='home'),
    path('page/<int:page>/', views.ArticleList.as_view(), name='home'),
    path('articles/<int:pk>/<slug:slug>/', views.ArticleDetail.as_view(), name='detail'),
    path('preview/<int:pk>/', views.ArticlePreview.as_view(), name='preview'),
    path('category/<int:pk>/<slug:slug>/', views.CategoryList.as_view() , name='category'),
    path('category/<int:pk>/<slug:slug>/page/<int:page>', views.CategoryList.as_view() , name='category'),
    path('author/<int:pk>/<slug:username>/', views.AuthorList.as_view() , name='author'),
    path('author/<int:pk>/<slug:username>/page/<int:page>', views.AuthorList.as_view() , name='author'),
]
