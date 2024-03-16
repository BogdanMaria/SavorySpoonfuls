from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField
from django.urls import reverse

# Create your models here.



class Recipe(models.Model):
    STATUS = (
    (0, "Draft"), 
    (1, "Published")
    )

    DIFFICULTY = (
        (0, "Easy"),
        (1, "Intermediate"),
        (2, "Expert"),
    )

    CATEGORY = (
        (0, "STATERS"),
        (1, "MAINS"),
        (2, "SIDES"),
        (3, "DESSERTS"),
        (4, "SNACKS"),    
    )
    title = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="recipes")
    updated_on = models.DateField(auto_now=True)
    created_on = models.DateField(auto_now_add=True)
    description = models.TextField()
    ingredients = models.TextField()
    method = models.TextField()
    featured_image = CloudinaryField('image', default='placeholder')
    prep_time = models.IntegerField()
    cook_time = models.IntegerField()
    serving = models.IntegerField()
    difficulty = models.IntegerField(choices=DIFFICULTY, default=0)
    category = models.IntegerField(choices=CATEGORY, default=0)
    excerpt = models.TextField(blank=True)
    status = models.IntegerField(choices=STATUS, default=0)
    is_public = models.BooleanField(default=False)

    class Meta:
        ordering = ['created_on']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('recipe-details', kwargs={'pk': self.slug})


class Comment(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='comments')
    name = models.CharField(max_length=80)
    body = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    approved = models.BooleanField(default=False)

    class Meta:
        ordering = ['created_on']

    def __str__(self):
        return f"Comment {self.body} by {self.name}"