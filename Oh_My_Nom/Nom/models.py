from django.db import models
from django.contrib import admin
#from django.template.defaultfilters import slugify

class Category(models.Model):
	name = models.CharField(max_length=128, unique=True)
	#slug = models.SlugField()

	#def save(self, *args, **kwargs):
	#	self.slug = slugify(self.name)
	#	super(Category, self).save(*args, **kwargs)
#
	#class Meta:
	#	verbose_name_plural = 'Categories'

	def __str__(self): 
		return self.name

class Page(models.Model):
	category = models.ForeignKey(Category)
	title = models.CharField(max_length=128)
	url = models.URLField()

	def __str__(self): 
		return self.title

class PageAdmin(admin.ModelAdmin):
	list_display = ('title', 'category', 'url')
