from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse, HttpResponseNotFound
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from main.models import Recipe, SavedRecipe
import random
from main.forms import RatingForm

#Index is the main page of the site
#the html document is stored in the 'templates/main' folder
def index(request):
	return render(request,"main/index.html")

def hotrestaurants(request):
	return render(request,"main/hotrestaurants.html")

def randomrecipes(request):
		recipes = []
		names = []
		count = 0
		
		#get random numbers and pick those indices as recipes (range of how many recipes you have)
		randList = random.sample(range(0,19),5)

		for r in Recipe.objects.all():
			if (count in randList):
				name = r.title
				slug = r.slug
				url = r.url
				recipes += [(slug,name)]
			count += 1
				
		return render(request,"main/randomrecipes.html",{"recipes":recipes})

def registersignin(request):
	registered = False
	context_dict={}
	if request.method == 'POST':
		if(request.POST.get("registerusername") and request.POST.get("registerpassword")):
			#This Executes when the register form has been completed
			username = request.POST.get("registerusername")
			password = request.POST.get("registerpassword")
			if " " in username:
				print("it's wrong")
				context_dict["register_error"] = "Cannot have a space in username. Try again:"
				return render(request,"main/registersignin.html",context = context_dict)
			try:
				User.objects.get(username=username)
				#The previous statement breaks the code when it cannot find the given user,
				#this code executes when someone tries to reregister a username
				context_dict["register_error"] = "An account with that username already exists"
			except:
				#This code executes when the username provided is new
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
			#This code executes when the sign in form has been completed
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

def signout(request):
	logout(request)
	return HttpResponseRedirect(reverse("main:index"))

def logged_in_or_redirect(view_function):
	def wrapper(*args,**kwargs):
		if not args[0].user.is_authenticated:
			return HttpResponseRedirect(reverse("main:registersignin"))
		return view_function(*args,**kwargs)
	return wrapper

@logged_in_or_redirect	
def myplaces(request):
	return render(request,"main/myplaces.html")

@logged_in_or_redirect
def myrecipes(request):
	user = None
	myrecipes = []
	user = request.user
	
	for recipe in SavedRecipe.objects.all():
		rList = str(recipe).split(" ")
		rec = rList[2:]
		strR = ""
		for el in rec:
			strR = strR +" " + el
		result = strR[1:]
		for original in Recipe.objects.all():
			if (result == original.title):
				if recipe.user == user:
					name = original.title
					slug = original.slug
					myrecipes += [(slug,name)]
	return render(request, 'main/myrecipes.html', {"myrecipes":myrecipes})


def test(request):
	return render(request,"main/test.html")

@logged_in_or_redirect
def save_recipe(request):
	context_dict = {}
	print("OMG")
	if request.method == "POST":
		print("Got a post request")
		recipe_title =  request.POST.get('recipe_title')
		print(recipe_title)
		if (recipe_title==None):
			print("recipe not found... this shouldnt happen")
			return HttpResponseNotFound("Go back")
			
		recipe = get_object_or_404(Recipe,title=recipe_title)
		print("Got da sweet recipe, gonna save it to the database")
		s = SavedRecipe.objects.get_or_create(recipe=recipe,user=request.user)[0]
		print("saving recipe object: ",s)
		s.save()
		print("saved the recipe, WELL DONE!")
		context_dict["recipe"] = recipe
		context_dict["message"] = "Recipe saved!"
		return render(request, "main/recipe.html", context_dict)
	else:
		print("ERROR!")
		return HttpResponse("")


def show_recipe(request, slug):
        context_dict = {}
        try:
                recipe = Recipe.objects.get(slug=slug)
                context_dict["recipe"] = recipe
        except Recipe.DoesNotExist:
                context_dict["recipe"] = None
        return render(request, 'main/recipe.html', context_dict)

@login_required
def add_rating(request):
	print("1st step")
	
	if request.method == "POST":
		print("Got post request")
		recipe_rating = request.POST.get('recipe_rating')
		
		
