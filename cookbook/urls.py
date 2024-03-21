from . import views
from django.urls import path

urlpatterns = [
    path('', views.Home.as_view(), name='home'),
    path('create/', views.RecipeCreateView.as_view(), name='create_recipe'),
    path('browserecipes/', views.RecipeList.as_view(), name='browse-recipes'),
    path('my_drafts/', views.UserDrafts.as_view(), name='drafts'),
    path('mycookbook/', views.UserRecipes.as_view(), name='mycookbook'),
    path('<slug:slug>/', views.RecipeDetail.as_view(), name='recipe_list'),
    path('<slug:slug>/update/', views.RecipeEditView.as_view(), name='edit_recipe'),
    path('<slug:slug>/delete/', views.RecipeDeleteView.as_view(), name='delete_recipe'),
    path('rate/<int:recipe_id>/<int:reting>', views.rate),
]

handler404 = "cookbook.views.page_not_found_view"