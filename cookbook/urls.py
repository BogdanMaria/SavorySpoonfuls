from . import views
from django.urls import path

urlpatterns = [
    path('', views.Home.as_view(), name='home'),
    path('browserecipes/', views.RecipeList.as_view(), name='browse-recipes'),
    path('<slug:slug>/', views.RecipeDetail.as_view(), name='recipe_list')
]