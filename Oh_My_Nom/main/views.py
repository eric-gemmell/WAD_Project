#Http imports
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.http import JsonResponse, HttpResponseRedirect, HttpResponse, HttpResponseNotFound
import json
#Login and user imports
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from main.models import UserInfo
#Hot restaurants imports
from main.GoogleServices import  GetLocation, GetRestaurantsFromLocation 
from main.models import Restaurant
#Random recipes imports
from main.models import Recipe, SavedRecipe
import random
from main.forms import RatingForm


#Index is the main page of the site
#the html document is stored in the 'templates/main' folder
def index(request):
	return render(request,"main/index.html")


def getlocation(request):
	#get location stuff here
	return JsonResponse(GetLocation(request))
	

def getrestaurants(request):
	if request.method == "POST":
		try:
			json_dict = json.loads(request.body.decode('utf-8'))
		except:
			return JsonResponse({"error":"poor request"})

		if("location" not in json_dict):
			return JsonResponse({"error":"no location associated to request"})
		location = json_dict["location"]
		restaurants = GetRestaurantsFromLocation(location = location)
		status = "ok" if (len(restaurants) > 0) else "not ok"
		return JsonResponse({"restaurants":restaurants,"status":status})

	return JsonResponse({"error":"incorrect request type, please use post..."})


def hotrestaurants(request):
	return render(request,"main/hotrestaurants.html")


def hotrestaurantclicked(request):
	if request.method == "POST":
		try:
			json_dict = json.loads(request.body.decode('utf-8'))
		except:
			return HttpResponse("Poor Json request object")
		if("place_id" not in json_dict):
			return HttpResponse("Incorrect parameters in json")
		print(json_dict)
		print("restaurant clicked! ;",json_dict["place_id"])
		if(request.user.is_authenticated):
			restaurant = Restaurant(user = request.user,place_id=json_dict["place_id"])
			restaurant.save()
			print("saved restaurant: ",restaurant)			
		#do user adding restaurant stuff here
		return JsonResponse({"status":"ok"})
	else:
		return HttpResponseRedirect(reverse('main:hotrestaurants'))


# Generates 5 random recipes for the user 
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
			location = request.POST.get("registerlocation")
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
				userInfo = UserInfo(user = user)
				userInfo.save()
				#print("\n\n Successfully saved user\n\n")
				if(location != None):
					userInfo.location = location
					userInfo.save()
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
				#print("Invalid login details: {0}, {1}".format(username, password))
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
	user = None
	myplaces = []
	user = request.user
	
	for restaurant in Restaurant.objects.all():
		print(restaurant)
		place_id = restaurant.place_id
		myplaces += [place_id]
		#rList = str(recipe).split(" ")
		#rec = rList[2:]
		#strR = ""
		#for el in rec:
		#	strR = strR +" " + el
		#result = strR[1:]
		#for original in Recipe.objects.all():
		#	if (result == original.title):
		#		if recipe.user == user:
		#			name = original.title
		#			slug = original.slug
		#			myrecipes += [(slug,name)]
	return render(request, 'main/myplaces.html', {"myplaces":myplaces})



# Displays the names of the recipes the user had saved when that user is logged in 
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


def getmyplaces(request):
	if(request.user.is_authenticated):
		if(request.method == "POST"):
			json_dict = json.loads(request.body.decode("utf-8"))
			if("page" in json_dict):
				if(json_dict["page"] != "undefined"):
					pass					
	return JsonResponse({"error":"unacceptable request"})
	

def test(request):
	return render(request,"main/test.html")


# Allows a logged in user to save a recipe and notifies them when it has been saved
@logged_in_or_redirect
def save_recipe(request):
	context_dict = {}
	if request.method == "POST":
		recipe_title =  request.POST.get('recipe_title')
		if (recipe_title==None):
			return HttpResponseNotFound("Go back")
			
		recipe = get_object_or_404(Recipe,title=recipe_title)
		s = SavedRecipe.objects.get_or_create(recipe=recipe,user=request.user)[0]
		s.save()
		context_dict["recipe"] = recipe
		context_dict["message"] = "Recipe saved!"
		return render(request, "main/recipe.html", context_dict)
	else:
		return HttpResponse("")


# Shows a recipe from the database
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
		
		
