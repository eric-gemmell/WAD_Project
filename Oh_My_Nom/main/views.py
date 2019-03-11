from django.shortcuts import render
from django.http import HttpResponse
from main.models import Category
from main.models import Page
from django.views.generic import TemplateView, ListView
import random

def index(request):
    category_list = Category.objects.all()
    page_list = Page.objects.all()
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
	
def show_recipes(request):
	recipes = []
	count = 0
	
	#get random numbers and pick those indices as recipes (range of how many recipes you have)
	randList = random.sample(range(0,19),3)

	for obj in Page.objects.all():
            if (count in randList):
                url = obj.url
                name = obj.title
                recipes += ["Try this: ","<a href=",url,">",name,"</a>","<br>"]
            count += 1

	return HttpResponse(recipes)



