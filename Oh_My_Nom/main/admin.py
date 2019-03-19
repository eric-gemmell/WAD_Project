from django.contrib import admin
from main.models import PageAdmin, Recipe, SavedRecipe, Rating, UserInfo

# Register your models here.

class PageAdmin(admin.ModelAdmin):
	list_display = ('title', 'url')
	
admin.site.register(Recipe)
admin.site.register(SavedRecipe)
admin.site.register(Rating)
admin.site.register(UserInfo)
