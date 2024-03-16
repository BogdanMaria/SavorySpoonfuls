from django import forms
from .models import Recipe
from django_summernote.widgets import SummernoteWidget


class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = '__all__'
        exclude = [
            'author', 
            'slug', 
            'updated_on', 
            'created_on', 
            'excerpt']

        labels = {
            'status': 'Save as Draft or Publish?',
            'is_public': 'Share it with the Community?',
        }

        widgets = {
            'description': SummernoteWidget(),
            'ingredients': SummernoteWidget(),
            'method': SummernoteWidget(),
        }