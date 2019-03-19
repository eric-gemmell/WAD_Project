#Http imports
from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponseRedirect, HttpResponse
from django.http import JsonResponse
import json
#Login and user imports
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from main.models import UserInfo
#Hot restaurants imports
from main.GoogleServices import  GetLocation, GetRestaurantsFromLocation 
from main.models import Restaurant


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

def randomrecipes(request):
	return render(request,"main/randomrecipes.html")

def registersignin(request):
	registered = False
	context_dict={}
	if request.method == 'POST':
		if(request.POST.get("registerusername") and request.POST.get("registerpassword")):
			#This Executes when the register form has been completed
			username = request.POST.get("registerusername")
			password = request.POST.get("registerpassword")
			location = request.POST.get("registerlocation")
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
	return render(request,"main/myplaces.html")

@logged_in_or_redirect
def myrecipes(request):
	return render(request,"main/myrecipes.html")

def getmyplaces(request):
	if(request.user.is_authenticated):
		if(request.method == "POST"):
			json_dict = json.loads(request.body.decode("utf-8"))
			if("page" in json_dict):
				if(json_dict["page"] != "undefined"):
					pass					
	return JsonResponse({"error":"unacceptable request")
def test(request):
	return render(request,"main/test.html")
