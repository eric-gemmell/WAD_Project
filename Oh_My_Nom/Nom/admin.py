from django.contrib import admin
from Nom.models import Category, Page, PageAdmin

#class CategoryAdmin(admin.ModelAdmin):
#	prepopulated_fields = {'slug':('name',)}

class PageAdmin(admin.ModelAdmin):
	list_display = ('title','category', 'url')

admin.site.register(Category)

admin.site.register(Page)
