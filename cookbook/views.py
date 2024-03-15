from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.views import generic, View
from .models import Recipe

# Create your views here.

class Home(generic.TemplateView):
    template_name = "index.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['newly_added_recipes'] = Recipe.objects.filter(status=1, is_public=True).order_by('-created_on')[:6]
        return context


class RecipeList(generic.ListView):
    model = Recipe
    queryset = Recipe.objects.filter(status=1, is_public=True).order_by("-created_on")
    template_name = "browse-recipes.html"
    paginate_by = 6


class RecipeDetail(View):
    def get(self, request, slug, *args, **kwargs):
        queryset = Recipe.objects.filter(status=1)
        recipe = get_object_or_404(queryset, slug=slug)
        comments = recipe.comments.filter(approved=True).order_by('created_on')

        return render(
            request,
            "recipe_list.html",
            {
                "recipe": recipe,
                "comments": comments
            }
        )