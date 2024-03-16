from django import forms
from .models import Recipe


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