from django.shortcuts import render
from django.http import HttpResponse
from main.models import Category
from main.models import Page

def index(request):
    category_list = Category.objects
    page_list = Page.objects
    context_dict = {'categories': category_list, 'pages':page_list}
    return render(request, 'main/index.html', context_dict)

def about(request):
	context_dict = {'boldmessage': "Nom says here is the about page"}
	return render(request, 'main/about.html', context=context_dict)


def show_category(request, category_name_slug):
	context_dict = {}

	try:
                category = Category.objects.get(slug=category_name_slug)
                pages = Page.objects.filter(category=category)
                context_dict['pages'] = pages
                context_dict['category'] = category
	except Category.DoesNotExist:
                context_dict['category'] = None
                context_dict['pages'] = None

	return render(request, 'main/category.html', context_dict) 
