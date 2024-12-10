from . import views
from django.urls import path
from django.contrib.auth import views as authViews
app_name = "auth"

urlpatterns = [
    path('', views.ArticleList.as_view(), name="home"),
    path('articles/create/', views.ArticleCreate.as_view(), name="create"),
    path('articles/update/<int:pk>', views.ArticleUpdate.as_view(), name="update"),
    path('articles/delete/<int:pk>', views.ArticleDelete.as_view(), name="delete"),
    path('profile/', views.Profile.as_view(), name="profile"),
    path('register/', views.RegFormCreateForm.as_view() , name="register_form"),
    path('reserve-list/', views.ReserveListView.as_view() , name="reserve-list"),
    path('reserve-send/<int:reserve_id>', views.ReserveListViewForm , name="reserve-send"),
]