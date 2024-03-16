from . import views
from django.urls import path

urlpatterns = [
    path('', views.Home.as_view(), name='home'),
    path('recipe/create/', views.RecipeCreateView.as_view(), name='create_recipe'),
    path('browserecipes/', views.RecipeList.as_view(), name='browse-recipes'),
    path('my_drafts/', views.UserDrafts.as_view(), name='drafts'),
    path('mycookbook/', views.UserRecipes.as_view(), name='mycookbook'),
    path('<slug:slug>/', views.RecipeDetail.as_view(), name='recipe_list'),
]