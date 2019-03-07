from django.shortcuts import render
from django.http import HttpResponse
from main.forms import UserForm, UserProfileForm
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse


#Index is the main page of the site
#the html document is stored in the 'templates/main' folder
def index(request):
	return render(request,"main/index.html")

def hotrestaurants(request):
	return render(request,"main/hotrestaurants.html")

def randomrecipes(request):
	return render(request,"main/randomrecipes.html")

def registersignin(request):
	registered = False
	if request.method == 'POST':
		user_form = UserForm(data=request.POST)
		profile_form = UserProfileForm(data=request.POST)
		if user_form.is_valid() and profile_form.is_valid():
			user = user_form.save()
			user.set_password(user.password)
			user.save()
			profile = profile_form.save(commit=False)
			profile.user = user
			registered = True
		else:
			print(user_form.errors, profile_form.errors)
	else:
		user_form = UserForm()
		profile_form = UserProfileForm()

	return render(request,"main/registersignin.html",{'user_form': user_form,'profile_form': profile_form,'registered': registered})

def tempsignin(request):
	if request.method == 'POST':
		username = request.POST.get('username')
		password = request.POST.get('password')
		user = authenticate(username=username, password=password)
		if user:
			if user.is_active:
				login(request, user)
				return HttpResponseRedirect(reverse('main:index'))
			else:	
				return HttpResponse("Your account is disabled.")
		else:
			print("Invalid login details: {0}, {1}".format(username, password))
			return HttpResponse("Invalid login details supplied.")
	else:
		return render(request, 'main/tempsignin.html', {})

def myplaces(request):
	return render(request,"main/myplaces.html")

def myrecipes(request):
	return render(request,"main/myrecipes.html")

def test(request):
	return render(request,"main/test.html")
