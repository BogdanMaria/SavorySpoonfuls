from django.shortcuts import render, get_object_or_404, reverse
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect, HttpResponse, HttpRequest
from django.db.models import Q
from django.views import generic, View
from .models import Recipe, Rating
from .forms import RecipeForm, CommentForm
from django.template.defaultfilters import slugify
from django.contrib import messages
from django.contrib.auth.models import AnonymousUser
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .filters import RecipeFilter


#Homepage view
class Home(generic.TemplateView):
    template_name = "index.html"
    
    #Retrieve the last 6 added recipes
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['newly_added_recipes'] = Recipe.objects.filter(status=1, is_public=True).order_by('-created_on')[:6]
        return context

#User cookbok view
class UserRecipes(generic.ListView):
    model = Recipe
    template_name = "cookbook.html"
    paginate_by = 6

    def get(self, request):
        #Search bar
        search_recipe = request.GET.get('search')
        # Category filter - django filter
        filter = RecipeFilter(request.GET, queryset=Recipe.objects.all()) 

        if search_recipe:
            queryset = Recipe.objects.filter(Q(title__icontains=search_recipe) | Q(ingredients__icontains=search_recipe), status=1, author=request.user.id).order_by("-created_on")
        elif filter:
            queryset = filter.qs.filter(status=1, author=request.user.id).order_by("-created_on")
        else:
            queryset = Recipe.objects.filter(status=1, author=request.user.id).order_by("-created_on")
        return render(
            request,
            self.template_name,
            {
                'user_recipes': queryset,
                "searched": search_recipe,
                "filter": filter,
                },
        )
        

#User drafts views
class UserDrafts(generic.ListView):
    model = Recipe
    template_name = "drafts.html"
    paginate_by = 12

    def get(self, request):
        queryset = Recipe.objects.filter(status=0, author=request.user.id).order_by("-created_on")
        queryset_dict = {'drafts': queryset}

        return render(
            request,
            self.template_name,
            queryset_dict,
        )


#Browse recipes view
class RecipeList(generic.ListView):
    model = Recipe
    template_name = "browse-recipes.html"
    paginate_by = 8

 # Search bar with Q objects implemented following:
    # https://stackpython.medium.com/django-search-with-q-objects-tutorial-9c701db74e0e
    def get_queryset(self):
        search_recipe = self.request.GET.get('search')
        # Category filter - django filter
        # https://medium.com/@balt1794/chapter-15-django-filters-6947da6df52a
        filter = RecipeFilter(self.request.GET, queryset=Recipe.objects.all())

        if search_recipe:
            queryset = Recipe.objects.filter(Q(title__icontains=search_recipe) | 
            Q(ingredients__icontains=search_recipe), status=1, is_public=True).order_by("-created_on")
        elif filter:
            queryset = filter.qs.filter(status=1, is_public=True).order_by("-created_on")
        else:
            queryset = Recipe.objects.filter(status=1, is_public=True).order_by("-created_on")
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = RecipeFilter(self.request.GET, queryset=Recipe.objects.all())
        context['searched'] = self.request.GET.get('search')
        return context


#Recipe detail view
class RecipeDetail(View):
    def get(self, request, slug, *args, **kwargs):
        queryset = Recipe.objects.filter(status=1)
        recipe = get_object_or_404(queryset, slug=slug)
        comments = recipe.comments.filter(approved=True).order_by('created_on')

        if request.user.is_authenticated:
            rating = Rating.objects.filter(recipe=recipe, user=request.user).first()
            recipe.user_rating = rating.rating if rating else 0

        return render(
            request,
            "recipe_list.html",
            {
                "recipe": recipe,
                "comments": comments,
                "comment_form": CommentForm(),
            }
        )
    #Save comment
    def post(self, request, slug, *args, **kwargs):
        queryset = Recipe.objects.filter(status=1)
        recipe = get_object_or_404(queryset, slug=slug)
        comments = recipe.comments.filter(approved=True).order_by("created_on")
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            comment_form.instance.name = request.user.username
            comment = comment_form.save(commit=False)
            comment.recipe = recipe
            comment.save()
        else:
            comment_form = CommentForm()

        return render(
            request,
            "recipe_list.html",
            {
                "recipe": recipe,
                "comments": comments,
                "commented": True,
                "comment_form": comment_form,
            },
        )


# API for rating
def rate(request: HttpRequest, recipe_id: int, rating: int) -> HttpResponse:
    recipe = Recipe.objects.get(id=recipe_id)
    Rating.objects.filter(recipe=recipe, user=request.user).delete()
    recipe.rating_set.create(user=request.user, rating=rating)
    return rate(request)


#CRUD - Create recipe view
class RecipeCreateView(CreateView):
    
    form_class = RecipeForm
    template_name = 'recipe_create.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.slug = slugify(form.instance.title)
        return super().form_valid(form)

    # Overwrite the absolute url reverse in the Recipe model 
    # Redirect differently based on recipe status (Published or draft)
    def get_success_url(self, **kwargs):
        if self.object.status == 0:
            return reverse_lazy('drafts')
        else:
            return reverse_lazy('recipe_list', kwargs={'slug': self.object.slug})


# CRUD - Update recipe view
class RecipeEditView(UpdateView):
    model = Recipe
    form_class = RecipeForm
    template_name = 'recipe_edit.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.slug = slugify(form.instance.title)
        return super().form_valid(form)

    def get_success_url(self, **kwargs):
        if self.object.status == 0:
            return reverse_lazy('drafts')
        else:
            return reverse_lazy('recipe_list', kwargs={'slug': self.object.slug})


#CRUD - Delete recipe view
class RecipeDeleteView(DeleteView):
    model = Recipe
    template_name = 'recipe_confirm_delete.html'
    def get_success_url(self):
        if self.object.status == 0:
            return reverse_lazy('drafts')
        else:
            return reverse_lazy('mycookbook')


#Custom 404 error view
def page_not_found_view(request, exception):

    return render(request, '404.html', status=404)