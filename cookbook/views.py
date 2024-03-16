from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.http import HttpResponse
from django.views import generic, View
from .models import Recipe
from .forms import RecipeForm
from django.template.defaultfilters import slugify
from django.contrib import messages
from django.views.generic.edit import CreateView, UpdateView, DeleteView

# Create your views here.

class Home(generic.TemplateView):
    template_name = "index.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['newly_added_recipes'] = Recipe.objects.filter(status=1, is_public=True).order_by('-created_on')[:6]
        return context


class UserRecipes(generic.ListView):
    model = Recipe
    template_name = "cookbook.html"
    paginate_by = 6

    def get(self, request):
        queryset = Recipe.objects.filter(status=1, author=request.user.id).order_by("-created_on")
        queryset_dict = {'user_recipes': queryset}

        return render(
            request,
            self.template_name,
            queryset_dict,
        )
        

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


# CRUD - Update
class RecipeEditView(UpdateView):
    model = Recipe
    form_class = RecipeForm
    template_name = 'recipe_edit.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.slug = slugify(form.instance.title)
        return super().form_valid(form)


class RecipeDeleteView(DeleteView):
    model = Recipe
    template_name = 'recipe_confirm_delete.html'
    success_url = reverse_lazy('mycookbook')


# class AddRecipe(View):
#     form_class = RecipeForm
#     template_name = 'add_recipe.html'
    # def get(self,request, *args, **kwargs):
    #     form = self.form_class

    #     return render(
    #         request,
    #         self.template_name,
    #         {
    #             "form" : form,
    #             "posted" : False,
    #         }
    #     )

    # def post(self, request, *args, **kwargs):
    #     form = RecipeForm(data=request.POST)

    #     if form.is_valid():
    #         form.instance.author = request.user
    #         form.instance.slug = slugify(form.instance.title)
    #         title = form.instance.title
    #         recipe = form.save(commit=False)
    #         recipe.save()
    #         return render(
    #             request,
    #             'add_recipe.html',
    #             {
    #                 'posted': True,
    #                 'title' : title,
    #             }
    #         )
    #     else:
    #         return render(
    #             request,
    #             'add_recipe.html',
    #             {
    #                 'form': form,
    #                 'failed': True,
    #                 'posted': False,
    #             }
    #         )


# class EditRecipe(UpdateView):
#     form_class = RecipeForm
#     template_name = 'edit_recipe.html'
#     success_url = '/thanks/'
#     def form_valid(self, form):
#         # This method is called when valid form data has been POSTed.
#         # It should return an HttpResponse.
        # return super().form_valid(form)