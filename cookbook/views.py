from django.shortcuts import render
from django.http import HttpResponse
from django.views import generic
from .models import Recipe

# Create your views here.

class RecipeList(generic.ListView):
    model = Recipe
    queryset = Recipe.objects.filter(status=1, is_public=True).order_by("-created_on")
    template_name = "browse-recipes.html"
    paginate_by = 6