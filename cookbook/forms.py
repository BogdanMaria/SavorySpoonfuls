from django import forms
from .models import Recipe, Comment
from django.forms import ModelForm, Textarea
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
            'excerpt',
            ]

        labels = {
            'status': 'Save as Draft or Publish?',
            'is_public': 'Share it with the Community?',
        }

        widgets = {
            'description': SummernoteWidget(),
            'ingredients': SummernoteWidget(),
            'method': SummernoteWidget(),
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('body',)
        widgets = {'body': Textarea(attrs={'rows': 2})}

        labels = {'body': ''}