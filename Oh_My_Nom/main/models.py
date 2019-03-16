from django.db import models
from django.contrib.auth.models import User
from django.contrib import admin
from django.template.defaultfilters import slugify

# Create your models here.
class UserProfile(models.Model):
	#Users need to contain the following attributes:
		#-A userName and Password
		#-An address so that we know where find their restaurants
		
	#on_delete = models.Cascade means that upon deleteing the profile, the user model that had been created
	# and that is associated here by a one to one relationship will be deleted as well.
	user = models.OneToOneField(User,on_delete=models.CASCADE,primary_key=True)
	address = models.CharField(max_length=128)
	recipes = models.CharField(max_length=500,default="")
	
	def __str__():
		return self.user.username

class Recipe(models.Model):
        title = models.CharField(max_length=128)
        url = models.URLField()
        slug = models.SlugField(unique=True,blank=True,null=True)

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
        return self.user.username + " saves " + self.recipe.name

