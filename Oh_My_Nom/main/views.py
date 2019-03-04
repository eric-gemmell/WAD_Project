from django.shortcuts import render
from django.http import HttpResponse

#Index is the main page of the site
#the html document is stored in the 'templates/main' folder
def index(request):
	return render(request,"main/index.html")

def test(request):
	return render(request,"main/test.html")
