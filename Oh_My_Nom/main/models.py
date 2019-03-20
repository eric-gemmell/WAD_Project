from django.db import models
from django.contrib.auth.models import User
from django.contrib import admin
from django.template.defaultfilters import slugify
from django.utils import timezone


class Recipe(models.Model):
        title = models.CharField(max_length=128, unique=True)
        url = models.URLField()
        slug = models.SlugField(blank=True,null=True)

        def save(self, *args, **kwargs):
                self.slug = slugify(self.title)
                super(Recipe, self).save(*args, **kwargs)

        def __str__(self):
                return self.title



class PageAdmin(admin.ModelAdmin):
	list_display = ('title','url')
	


class SavedRecipe(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe,on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username + " saves " + self.recipe.title


class Rating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    recipe = models.ForeignKey(SavedRecipe, on_delete=models.CASCADE)

    date = models.DateTimeField()
    description = models.CharField(max_length=100)
    overall = models.CharField(max_length=100)
    
    def __str__(self):
        return self.description


class UserInfo(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	location = models.CharField(max_length=128)

	def __str__(self):
		return self.user.username + "; location: "+ self.location

class Restaurant(models.Model):
	user = models.ForeignKey(User,on_delete=models.CASCADE)
	place_id = models.CharField(max_length=200)

	def __str__(self):
		return "User '{}' saved restaurant: {}".format(self.user.username,self.place_id)
