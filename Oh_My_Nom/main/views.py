from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
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
	context_dict={}
	if request.method == 'POST':
		if(request.POST.get("registerusername") and request.POST.get("registerpassword")):
			print("\n\n GOT REGISTER INFORMATION \n\n")
			username = request.POST.get("registerusername")
			password = request.POST.get("registerpassword")
			try:
				User.objects.get(username=username)
				print("\n\nNON UNIQUE USERNAME")
				context_dict["register_error"] = "An account with that username already exists"
			except:
				print("\n\nUNIQUE USERNAME")
				user = User(username=username)
				user.save()
				#STILL need to check if password meets minum requirements
				#CHECK IF PASSWORD IS GOOD HERE
				user.set_password(password)
				user.save()
				print("\n\n Successfully saved user\n\n")
				user = authenticate(username=username, password=password)
				if user:
					 if user.is_active:
                                		login(request, user)
                                		return HttpResponseRedirect(reverse('main:index'))

		elif(request.POST.get("signinusername") and request.POST.get("signinpassword")):
			print("\n\n GOT SIGNIN INFORMATION \n\n")
			username = request.POST.get('signinusername')
			password = request.POST.get('signinpassword')
			user = authenticate(username=username, password=password)
			if user:
				if user.is_active:
					login(request, user)
					return HttpResponseRedirect(reverse('main:index'))
				else:
					context_dict["signin_error"] = "Your account is disabled"
			else:
				print("Invalid login details: {0}, {1}".format(username, password))
				context_dict["signin_error"] = "Incorrect login details"
		
	return render(request,"main/registersignin.html",context = context_dict)

def signin(request):
	print("received request in sign in !")
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
		return HttpResponseRedirect(reverse("main:index"))

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

def tempsignout(request):
	logout(request)
	return HttpResponseRedirect(reverse("main:index"))

def myplaces(request):
	return render(request,"main/myplaces.html")

def myrecipes(request):
	if not request.user.is_authenticated:
		return HttpResponseRedirect(reverse("main:tempsignin"))
	return render(request,"main/myrecipes.html")

def test(request):
	return render(request,"main/test.html")
