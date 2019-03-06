from django.shortcuts import render
from django.http import HttpResponse

#Index is the main page of the site
#the html document is stored in the 'templates/main' folder
def index(request):
	return render(request,"main/index.html")

def hotrestaurants(request):
	return render(request,"main/hotrestaurants.html")

def randomrecipes(request):
	return render(request,"main/randomrecipes.html")

def registersignin(request):
	return render(request,"main/registersignin.html")

def myplaces(request):
	return render(request,"main/myplaces.html")

def myrecipes(request):
	return render(request,"main/myrecipes.html")

def test(request):
	return render(request,"main/test.html")
