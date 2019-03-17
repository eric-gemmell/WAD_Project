from django.contrib import admin
from main.models import PageAdmin, Recipe, SavedRecipe, UserProfile, Rating

# Register your models here.

class PageAdmin(admin.ModelAdmin):
	list_display = ('title', 'url')
	
admin.site.register(UserProfile)
admin.site.register(Recipe)
admin.site.register(SavedRecipe)
admin.site.register(Rating)
