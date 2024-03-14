from . import views
from django.urls import path

urlpatterns = [
    path('browse-recipes/', views.RecipeList.as_view(), name='browse-recipes'),
]