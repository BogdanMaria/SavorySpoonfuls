from . import views
from django.urls import path

urlpatterns = [
    path('', views.Home.as_view(), name='home'),
    path('add_recipe/', views.AddRecipe.as_view(), name='add_recipe'),
    path('browserecipes/', views.RecipeList.as_view(), name='browse-recipes'),
    path('drafts/', views.UserDrafts.as_view(), name='drafts'),
    path('mycookbook/', views.UserRecipes.as_view(), name='mycookbook'),
    path('<slug:slug>/', views.RecipeDetail.as_view(), name='recipe_list'),
]