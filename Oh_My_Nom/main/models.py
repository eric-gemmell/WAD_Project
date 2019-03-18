from django.db import models
from django.contrib.auth.models import User
from django.contrib import admin
from django.template.defaultfilters import slugify
from django.utils import timezone

# Create your models here.
class UserProfile(models.Model):
	#Users need to contain the following attributes:
		#-A userName and Password
		#-An address so that we know where find their restaurants
		
	#on_delete = models.Cascade means that upon deleteing the profile, the user model that had been created
	# and that is associated here by a one to one relationship will be deleted as well.
	user = models.OneToOneField(User,on_delete=models.CASCADE,primary_key=True)
	address = models.CharField(max_length=128)
	
	def __str__():
		return self.user.username

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
    describtion = models.CharField(max_length=100)
    dishType = models.CharField(max_length=100)
    price = models.CharField(max_length=100)
    fanciness = models.CharField(max_length=100)
    firstDate = models.CharField(max_length=100)
    lazyNight = models.CharField(max_length=100)
    difficulty = models.CharField(max_length=100)
    dishType = models.CharField(max_length=100)
    price = models.CharField(max_length=100)
    veggie = models.CharField(max_length=100)
    overall = models.CharField(max_length=100)
    
    def __str__(self):
        return self.description

