from django import forms
from .models import Recipe
from django_summernote.widgets import SummernoteWidget


class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = [
            'title',
            'description',
            'ingredients',
            'method',
            'featured_image',
            'prep_time',
            'cook_time',
            'serving',
            'difficulty',
            'category',
            'status',
            'is_public',
            ]
        widgets = {
        'description': SummernoteWidget(),
        'ingredients': SummernoteWidget(),
        'method': SummernoteWidget(),
        }