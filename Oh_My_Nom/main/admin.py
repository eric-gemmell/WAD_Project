from django.contrib import admin
from main.models import UserProfile
from main.models import Category, Page, PageAdmin

# Register your models here.

class PageAdmin(admin.ModelAdmin):
	list_display = ('title','category', 'url')
	
admin.site.register(UserProfile)
admin.site.register(Category)
admin.site.register(Page)
